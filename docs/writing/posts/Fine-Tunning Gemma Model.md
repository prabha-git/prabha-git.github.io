---
draft: true
date: 2024-03-06
slug: tokenizer-comparison
tags:
  - llm
authors:
  - Prabha
---
!!!note "Self Note"
	This note is for myself, writing help me solidify my understanding


## Gemma using KerasNLP

Original Notebook: [Get started with Gemma using KerasNLP](https://www.kaggle.com/code/nilaychauhan/get-started-with-gemma-using-kerasnlp)

- KerasNLP is a collection of NLP models implemented in Keras and runnable on JAX, PyTourch and TenserFlow
- Checkout [[intro-to-keras-for-engineers]] for Keras basics
	- Keras is a high-level, multi-framework deep learning API designed for simplicity and ease of use
- KerasNLP provides an implementation of popular [architectures](https://keras.io/api/keras_nlp/models/)
	- Models can be created in two ways
		- from_preset() constructor, instantiates with pre-trained config
		- custom config controlled by the user.
- In this notebook, we created model using `GemmaCasualLM` , an end-to-end casual language modeling. causal language model predicts next token.

```python
gemma_lm = keras_nlp.models.GemmaCausalLM.from_preset("gemma_2b_en")
```

```python
# Summary provides a nice summary of the model
gemma_lm.summary()


# To generate text
gemma_lm.generate("What is the meaning of life?", max_length=64)

# You can also provide batched prompts using a list as input:
gemma_lm.generate(
    ["What is the meaning of life?",
     "How does the brain work?"],
    max_length=64)
```



-----

## Fine-tunning Gemma in Keras using LoRA

[Kaggle: Your Home for Data Science](https://www.kaggle.com/code/prabhakaran/fine-tune-gemma-models-in-keras-using-lora/edit) 
[Original Notebook](https://www.kaggle.com/code/nilaychauhan/fine-tune-gemma-models-in-keras-using-lora)

- Gemma is a lightweight open-source model from Google
- Pre-training helps LLMs learn general-purpose knowledge
- It can be fine-tuned with domain-specific to perform specific tasks (such as sentimental analysis)
- LLMs are extremely large, and full fine-tuning is expensive, also fine-tuning datasets are smaller.
- [LoRA](https://arxiv.org/abs/2106.09685) technique keeps original weights and inserts a small number of new weights into the model.
- This example uses [[Keras]] to perform LoRA fine-tuning


```python
import os
os.environ["KERAS_BACKEND"] = "jax"  # Or "torch" or "tensorflow".
os.environ["XLA_PYTHON_CLIENT_MEM_FRACTION"]="1.00"

import keras
import keras_nlp

import json

with open('./databricks-dolly-15k.jsonl') as file:
	for line in file:
	features = json.loads(line)
	# Filter out examples with context, to keep it simple.
	if features["context"]:
		continue
		# Format the entire example as a single string.
		template = "Instruction:\n{instruction}\n\nResponse:\n{response}"
		data.append(template.format(**features))

data = data[:1000]



gemma_lm = keras_nlp.models.GemmaCausalLM.from_preset("gemma_2b_en")
```

it downloads these files

![[Pasted image 20240316224221.png]]


Running Gemma using Keras and Colab
[Google Colab](https://colab.research.google.com/drive/1msMLKjOv5ZyXoloHqUuESNztrdQ1cE7u#scrollTo=g_eZd0vII2yM)

```python
import keras

import keras_nlp

import kaggle

gemma_lm = keras_nlp.models.GemmaCausalLM.from_preset("gemma_2b_en")
gemma_lm.generate("What is the biggest city in USA?", max_length=30)
```


Output:
```text
What is the biggest city in USA?\n\nWhat is the capital of USA?\n\nWhat is the largest city in USA?\n\nWhat is the
```


!!!note "Note"
	Since this is not instruction-tuned, it tries to predict the next word. Not helpful.


### LoRA Fine-tuning

[Google Colab](https://colab.research.google.com/drive/1msMLKjOv5ZyXoloHqUuESNztrdQ1cE7u#scrollTo=g_eZd0vII2yM)

We used [Databricks Dolly 15k dataset for finetuning](https://www.kaggle.com/datasets/databricks/databricks-dolly-15k)

- LoRA rank determines the dimensionality of trainable matrices that are added to the original weights of LLM.
- A higher rank means more detailed changes with more trainable parameters. Lower rank means less computational overhead with less precise adaptation.
- In practice start with a small rank such as 4.


Inference after rank=4 fine-tuning

```python
>>gemma_lm.backbone.enable_lora(rank=4)
>>.....
>>gemma_lm.generate("What is the biggest city in USA?", max_length=60)
What is the biggest city in USA? This question has been the subject of much debate. Some people say that New York City is the biggest city in US while others say that Los Angeles is the biggest city in the US.

There are many factors that go into determining which city is the biggest
```


```python
gemma_lm.backbone.enable_lora(rank=5)
>>.....
>>gemma_lm.generate("What is the biggest city in USA?", max_length=60)
What is the biggest city in USA?

The largest city in the United States is New York City, with a population of 8,509,700 as per the 2020 census.

How do you find the biggest city of USA?

How do
```