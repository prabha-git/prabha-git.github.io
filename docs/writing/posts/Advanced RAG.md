---
draft: false
date: 2024-03-23
slug: advanced-rag-notes
tags:
  - llm
authors:
  - Prabha
---
!!!note "Self Note"
	This note is for me to understand the concepts
	
[Advanced Retrieval-Augmented Generation: From Theory to LlamaIndex Implementation | by Leonie Monigatti | Feb, 2024 | Towards Data Science](https://towardsdatascience.com/advanced-retrieval-augmented-generation-from-theory-to-llamaindex-implementation-4de1464a9930)

	Summary
		- Advanced techniques can be categorized into `Pre-Retrieval`, `Retrieval`, `Post-Retrieval`


		- Pre-Retrieval
			- Focuses on data indexing optimization & Query optimization
			- Data indexing optimization stores data for efficient retrieval, some strategies below
				- Sliding Window
				- Data cleaning, Factual accuracy, etc.
				- Adding metadata
				- Optimizing index structure such as adjusting chunk sizes, and multi-indexing strategies.
