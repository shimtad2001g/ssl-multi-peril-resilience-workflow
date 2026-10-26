import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

fig, ax = plt.subplots(figsize=(16, 8))
ax.set_xlim(0, 16)
ax.set_ylim(0, 8)
ax.axis('off')

plt.text(8, 7.5, "Figure 1: Integrated Synergistic Methodological Workflow", fontsize=20, fontweight='bold', ha='center')

rect1 = patches.FancyBboxPatch((0.5, 4.5), 3, 2, boxstyle="round,pad=0.2", edgecolor="#005b96", facecolor="#e6f2ff", lw=2)
ax.add_patch(rect1)
plt.text(2.0, 6.0, "Phase 1: Unified Data\nAcquisition", fontsize=14, fontweight='bold', ha='center', color="#005b96")
plt.text(2.0, 5.0, "• GEE API\n• Optical (Sentinel-2)\n• SAR (Sentinel-1)\n• Climate & Topography", fontsize=11, ha='center', va='center')

rect2 = patches.FancyBboxPatch((4.5, 4.5), 3.5, 2, boxstyle="round,pad=0.2", edgecolor="#029386", facecolor="#e6fcf5", lw=2)
ax.add_patch(rect2)
plt.text(6.25, 6.0, "Phase 2: Multi-Modal SSL", fontsize=14, fontweight='bold', ha='center', color="#029386")
plt.text(6.25, 5.0, "• Optical Branch: SimCLR\n  (Contrastive Learning)\n• SAR Branch: FloodSSL\n  (CNN Encoder)", fontsize=11, ha='center', va='center')

rect3 = patches.FancyBboxPatch((9.0, 4.5), 3.0, 2, boxstyle="round,pad=0.2", edgecolor="#d97706", facecolor="#fef3c7", lw=2)
ax.add_patch(rect3)
plt.text(10.5, 6.0, "Phase 3: Risk Mitigation\n& MCDA", fontsize=14, fontweight='bold', ha='center', color="#d97706")
plt.text(10.5, 5.0, "• Dual-Trigger Payout\n  (VCI < 30%)\n• Synergistic NBS\n  Targeting", fontsize=11, ha='center', va='center')

rect4 = patches.FancyBboxPatch((13.0, 4.5), 2.5, 2, boxstyle="round,pad=0.2", edgecolor="#6b21a8", facecolor="#f3e8ff", lw=2)
ax.add_patch(rect4)
plt.text(14.25, 6.0, "Phase 4: Operational\nDeliverables", fontsize=14, fontweight='bold', ha='center', color="#6b21a8")
plt.text(14.25, 5.0, "• Automated Maps\n• GeoTIFFs\n• Interactive\n  Dashboard", fontsize=11, ha='center', va='center')

ax.add_patch(patches.FancyArrowPatch((3.6, 5.5), (4.4, 5.5), arrowstyle='->', mutation_scale=20, lw=2, color='gray'))
ax.add_patch(patches.FancyArrowPatch((8.1, 5.5), (8.9, 5.5), arrowstyle='->', mutation_scale=20, lw=2, color='gray'))
ax.add_patch(patches.FancyArrowPatch((12.1, 5.5), (12.9, 5.5), arrowstyle='->', mutation_scale=20, lw=2, color='gray'))

banner = patches.FancyBboxPatch((1.0, 1.0), 14.0, 1.5, boxstyle="round,pad=0.1", edgecolor="#dc2626", facecolor="#fee2e2", lw=2)
ax.add_patch(banner)
plt.text(8.0, 1.75, "CORE INNOVATION:\nReplacing expensive field ground-truthing with Self-Supervised Deep Learning (SSL)\non unlabeled satellite imagery.", 
         fontsize=14, fontweight='bold', ha='center', va='center', color="#dc2626")

out_path = os.path.expanduser("~\\Desktop\\ssl-multi-peril-resilience-workflow\\Phase4_Deliverables\\Figure1_Workflow_Diagram_Final.png")
plt.savefig(out_path, dpi=300, bbox_inches='tight', facecolor='white')
plt.close()

print("=== FIGURE 1 CORRECTED AND SAVED ===")