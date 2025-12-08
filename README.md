# Analyzing the Relationship of Crewed Space Habitat Construction Technologies Using SBERT-based Semantic Similarity

**Key Words** : `Crewed Space Habitat Construction`, `Technology Relationship`, `Semantic Similarity`, `Network Analysis`

---

## ABSTRACT
Crewed space habitat construction is a multidisciplinary endeavor that involves complex interactions among various technologies. This complexity necessitates robust R&D strategies informed by a thorough analysis of the relationships between these technologies. However, traditional qualitative approaches and hierarchical classification methods have struggled to capture the deep semantic relationships and many-to-many interdependencies among technologies. This study addresses these limitations by integrating SBERT (Sentence-BERT)-based semantic similarity measurement with network science techniques. We conducted a quantitative analysis to measure the semantic similarities among 87 technologies related to crewed space habitat construction and organized their relationships into a network format. Through this analysis, we identified clusters of functionally related technologies and key technologies that exhibit high centrality within the network. The findings from this quantitative relationship analysis provide a foundation for future technology roadmap design and help identify potential areas for interdisciplinary research.

## Workflow
#### 1. Semantic Network Generation
  - Generates high-dimensional vectors from concatenated technology descriptions using SBERT (all-MiniLM-L12-v2)
  - Nodes represent technologies, and edges are established based on a cosine similarity threshold of 0.6
#### 2. Community Detection
  - Applies the Louvain method to detect modular communities of functionally related technologies
  - Differentiates connection strengths using solid lines for strong relationships and dashed lines for moderate ones
#### 3. Centrality Analysis
  - Evaluates node importance using Degree, Betweenness, and Closeness centrality
  - Applies Min-Max normalization to centrality scores to identify and rank core technologies within the network


## Data Structure
| Column Name | Description |
| :--- | :--- |
| **code** |Unique identifier for the technology (e.g., `A01`) |
| **기술명** (Tech Name) | Name of the technology |
| **대분류** (Category Name) | Main category of the technology (Used for color grouping) |
| **overview** | General description of the technology |
| **necessity** | Explanation of why the technology is needed |
| **subtech** | Details of sub-technologies or specific components |

> The `overview`, `necessity`, and `subtech` columns are concatenated to form the input text for the SBERT model.
