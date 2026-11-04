
import torch
import torch.nn as nn
import torch.nn.functional as F


class TransformerBlock(nn.Module):
    def __init__(self, d_model, n_heads, d_ff):
        super().__init__()

        assert d_model % n_heads == 0

        self.d_model = d_model
        self.n_heads = n_heads
        self.d_k = d_model // n_heads

        # Q, K, V projections
        self.W_q = nn.Linear(d_model, d_model)
        self.W_k = nn.Linear(d_model, d_model)
        self.W_v = nn.Linear(d_model, d_model)
        self.W_o = nn.Linear(d_model, d_model)

        # Feed-Forward Network
        self.fc1 = nn.Linear(d_model, d_ff)
        self.fc2 = nn.Linear(d_ff, d_model)

        # Layer Normalization
        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)

    def forward(self, x, attention_mask=None, verbose=False):
        B, T, D = x.shape

        def show(name, tensor):
            if verbose:
                print(f"{name:<30} {tuple(tensor.shape)}")

        show("Input X:", x)

        # =====================================
        # 1. Q, K, V projections
        # =====================================

        Q = self.W_q(x)
        K = self.W_k(x)
        V = self.W_v(x)

        show("Q before split:", Q)
        show("K before split:", K)
        show("V before split:", V)

        # Split into multiple heads
        Q = Q.reshape(
            B, T, self.n_heads, self.d_k
        ).transpose(1, 2)

        K = K.reshape(
            B, T, self.n_heads, self.d_k
        ).transpose(1, 2)

        V = V.reshape(
            B, T, self.n_heads, self.d_k
        ).transpose(1, 2)

        show("Q after split:", Q)
        show("K after split:", K)
        show("V after split:", V)

        # =====================================
        # 2. Attention scores
        # =====================================

        scores = Q @ K.transpose(-2, -1)
        scores = scores / (self.d_k ** 0.5)

        show("Attention scores:", scores)

        # =====================================
        # 3. Padding Attention Mask
        # =====================================

        key_mask = None

        if attention_mask is not None:
            assert attention_mask.shape == (B, T)

            attention_mask = attention_mask.to(
                device=x.device, dtype=torch.bool
            )

            # (B, T) -> (B, 1, 1, T)
            key_mask = attention_mask[:, None, None, :]

            # Mask padding keys before softmax.
            # Finite minimum avoids NaNs for all-PAD samples.
            scores = scores.masked_fill(
                ~key_mask,
                torch.finfo(scores.dtype).min
            )

            show("Attention mask:", key_mask)
            show("Masked scores:", scores)

        # =====================================
        # 4. Softmax
        # =====================================

        weights = F.softmax(scores, dim=-1)

        if key_mask is not None:
            # Also handles sequences containing only PAD.
            weights = weights.masked_fill(
                ~key_mask, 0.0
            )

        show("Attention weights:", weights)

        # =====================================
        # 5. Attention output
        # =====================================

        attn_output = weights @ V

        show("Attention output per head:", attn_output)

        # Concatenate heads
        attn_output = attn_output.transpose(
            1, 2
        ).contiguous().reshape(B, T, D)

        show("Concatenated heads:", attn_output)

        # Output projection
        attn_output = self.W_o(attn_output)

        show("Attention projection:", attn_output)

        # =====================================
        # 6. Residual + LayerNorm
        # =====================================

        x = self.norm1(x + attn_output)

        show("After Residual + Norm 1:", x)

        # =====================================
        # 7. Feed-Forward Network
        # =====================================

        hidden = F.relu(self.fc1(x))

        show("FFN hidden:", hidden)

        ff_output = self.fc2(hidden)

        show("FFN output:", ff_output)

        # =====================================
        # 8. Residual + LayerNorm
        # =====================================

        output = self.norm2(x + ff_output)
        if attention_mask is not None:
            output = output.masked_fill(
                ~attention_mask.unsqueeze(-1), 0.0
            )

        show("Final output:", output)

        return output
