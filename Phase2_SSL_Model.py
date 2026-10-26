import os
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torchvision import transforms
import rasterio
from rasterio.plot import reshape_as_image
import numpy as np

# 1. Define the CNN Encoder
class SSL_Encoder(nn.Module):
    def __init__(self):
        super(SSL_Encoder, self).__init__()
        self.conv1 = nn.Conv2d(3, 32, kernel_size=3, stride=1, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        self.fc = nn.Linear(64 * 16 * 16, 128)
        
    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = x.reshape(x.size(0), -1) # <--- FIX: Changed .view() to .reshape()
        x = self.fc(x)
        return F.normalize(x, dim=1)

# 2. Contrastive Loss (NT-Xent)
def contrastive_loss(z_i, z_j, temperature=0.5):
    batch_size = z_i.size(0)
    z = torch.cat([z_i, z_j], dim=0)
    sim_matrix = torch.exp(torch.mm(z, z.t().contiguous()) / temperature)
    mask = (torch.ones_like(sim_matrix) - torch.eye(2 * batch_size, device=sim_matrix.device)).bool()
    sim_matrix = sim_matrix.masked_select(mask).view(2 * batch_size, -1)
    pos_sim = torch.exp(torch.sum(z_i * z_j, dim=-1) / temperature)
    pos_sim = torch.cat([pos_sim, pos_sim], dim=0)
    loss = (- torch.log(pos_sim / sim_matrix.sum(dim=-1))).mean()
    return loss

# 3. Load Real Data
def load_real_data():
    base_path = os.path.expanduser("~\\Desktop\\ssl-multi-peril-resilience-workflow\\Phase1_Data_Acquisition")
    s2_path = os.path.join(base_path, "Sentinel2_Optical.tif")
    
    with rasterio.open(s2_path) as src:
        img = src.read()
        img = reshape_as_image(img)
        img = img.astype(np.float32) / 255.0
        
    tensor_img = torch.tensor(img).permute(2, 0, 1)
    tensor_img = tensor_img[:, :64, :64]
    return tensor_img.unsqueeze(0)

# 4. Augmentation Pipeline
augmentation = transforms.Compose([
    transforms.RandomResizedCrop(64, scale=(0.5, 1.0)),
    transforms.RandomHorizontalFlip(),
    transforms.ColorJitter(brightness=0.4, contrast=0.4, saturation=0.4, hue=0.1)
])

# 5. Training Loop
def train_ssl():
    print("Initializing SSL Encoder...")
    device = torch.device("cpu")
    model = SSL_Encoder().to(device)
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    
    print("Loading real satellite imagery...")
    real_image = load_real_data().to(device)
    
    epochs = 3
    print(f"Starting Contrastive Pretraining for {epochs} epochs...")
    
    model.train()
    for epoch in range(epochs):
        optimizer.zero_grad()
        
        view_1 = augmentation(real_image)
        view_2 = augmentation(real_image)
        
        z_i = model(view_1)
        z_j = model(view_2)
        
        loss = contrastive_loss(z_i, z_j)
        
        loss.backward()
        optimizer.step()
        
        print(f"Epoch [{epoch+1}/{epochs}], Contrastive Loss: {loss.item():.4f}")
        
    save_path = os.path.expanduser("~\\Desktop\\ssl-multi-peril-resilience-workflow\\Phase2_SSL_Models\\SSL_Encoder_Weights.pth")
    torch.save(model.state_dict(), save_path)
    print(f"Phase 2 Complete! Encoder weights saved to: {save_path}")

if __name__ == "__main__":
    train_ssl()
