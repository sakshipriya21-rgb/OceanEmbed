import torch
import torch.nn as nn


# ---------------------------------------------------
# OceanEmbed Encoder-Decoder Model
# ---------------------------------------------------

class OceanEmbed(nn.Module):

    def __init__(self):

        super().__init__()

        # ---------------------------------------------------
        # Encoder
        # ---------------------------------------------------

        self.encoder = nn.Sequential(

            nn.Linear(7, 32),

            nn.ReLU(),

            nn.Linear(32, 16)
        )

        # ---------------------------------------------------
        # Decoder
        # ---------------------------------------------------

        self.decoder = nn.Sequential(

            nn.Linear(16, 32),

            nn.ReLU(),

            nn.Linear(32, 15)
        )


    # ---------------------------------------------------
    # Forward pass
    # ---------------------------------------------------

    def forward(self, x):

        embedding = self.encoder(x)

        output = self.decoder(embedding)

        return output


    # ---------------------------------------------------
    # Extract embedding
    # ---------------------------------------------------

    def get_embedding(self, x):

        return self.encoder(x)