# Building a Recommendation System with Vectors

## 1. The Problem
How do Amazon, Netflix, etc. know what to suggest next?

| Attempt | Idea | Fatal Flaw |
|---------|------|------------|
| **Manual Arrays** | Put “similar” items in the same bucket (all gym gear in one list). | Doesn’t scale; rigid boundaries (banana → fruit **and** gym-snack). |
| **Graph / Co-occurrence** | Link items that are frequently bought together (diapers ↔ beer). | **Cold-start**: brand-new whey protein has zero edges, so it’s never recommended even though it’s semantically identical to existing proteins. |

## 2. The Solution: Multi-Dimensional Vectors
Represent every item as an array of numbers across hundreds or thousands of semantic dimensions.

| Example | Dimensions |
|---------|------------|
| **Netflix movie** | Action: 10, Comedy: −5, Romance: 2, Realism: −7, … |
| **Amazon product** | Protein: 9, Vegan: −8, Price: 0.2, Gym: 8.5, … |

These arrays are **vectors**; the conversion from raw data → vector is called **embedding** and is done by a neural network.

## 3. Semantic Arithmetic
Because vectors encode meaning, you can do math on concepts:

```math
\text{King} - \text{Man} + \text{Woman} ≈ \text{Queen}
```

Subtract “maleness”, add “femaleness”, land exactly on “Queen” ⇒ the system truly **understands** traits, not just keywords.

## 4. Measuring Similarity
To recommend, find vectors **closest** to the user’s current vector.

| Method | What it tells us | Used when |
|--------|------------------|-----------|
| **Euclidean distance** | Straight-line length between points | Raw closeness in space |
| **Cosine similarity** | Angle between vectors (direction) | Preferred in AI/NLP; ignores vector length and captures **semantic alignment** |