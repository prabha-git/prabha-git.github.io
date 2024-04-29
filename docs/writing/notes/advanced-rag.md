---
draft: true
date: 2024-03-23
slug: advanced-rag-notes
tags:
  - llm
authors:
  - Prabha
---
# Advanced RAG

!!!note "Self Note"
	This note is for me to understand the concepts
	
## [Advanced Retrieval-Augmented Generation: From Theory to LlamaIndex Implementation | by Leonie Monigatti | Feb, 2024 | Towards Data Science](https://towardsdatascience.com/advanced-retrieval-augmented-generation-from-theory-to-llamaindex-implementation-4de1464a9930)

### Summary
Advanced techniques can be categorized into `Pre-Retrieval`, `Retrieval`, `Post-Retrieval`


- Pre-Retrieval
	- Focuses on data indexing optimization & Query optimization
	- Data indexing optimization stores data for efficient retrieval, some strategies below
		- Sliding Window
		- Data cleaning, Factual accuracy, etc.
		- Adding metadata
		- Optimizing index structure such as adjusting chunk sizes, and [multi-indexing strategies.](https://twitter.com/CShorten30/status/1725151347756990563)
			


- Retrieval Optimization
	- This stage aims to identify the most relevant context. 
	- Usually based on vector search, important is to select the right embedding model.
		- Fine-tuning embedding models [Guide](https://betterprogramming.pub/fine-tuning-your-embedding-model-to-maximize-relevance-retrieval-in-rag-pipeline-2ea3fa231149)
		- Dynamic Embedding,`embeddings-ada-02` is an example of this.


- Post-Retrieval Optimization
	- Helps stay within context limits & reduces noise
		- Few techniques are 
			- Prompt Compression - removes irrelevant and highlights important info
			- Re-ranking - using machine learning model to recalculate relevance score


### \[Exercise\] Implementing Advanced RAG using LlamaIndex

[Colab link for exercise](https://colab.research.google.com/drive/1_zoaHmFLaBc8FXxEGlHsgCs4blTtFNuD?usp=sharing)


