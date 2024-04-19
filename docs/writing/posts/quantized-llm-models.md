---
draft: false
date: 2024-04-19
slug: quantized-llm-models
tags:
  - llm
authors:
  - Prabha
---

# Quantized LLM Model

LLM models are large with billions of parameter, 

for example, Open source Models like llama2 comes in the sizes 7B, 13B and 70B

Google's Gemma is 2B

Even though OpenAI's GPT4 is not opensource or it's architecture is publically shared. It is speculatted to have more than Trillion parameters with 8 models working together (mixture of experts)

## What is a parameter?

Parameter is a model weight it learned during the training phase , number of parameter can be a rough indicator of model capability and complexity. 

these parameters will be used in a huge matrix multiplication on each layers until it produces an output.


# What is the problem LLMs

As the model is huge with billions of parameter, you need to load all the paramters in it's memory and perform huge matrix multiplication. 

Lets do the math 

lets say 70B parameter model (like llama2-70b model). Default size in which these parameters are stores is 32bit (4 bytes)

to load this model , you need 70B * 4 bytes = 260.77GB of memory

Now you see the problem, correct.


What is Quantization?

Quantization is a method to reduce the size of the model, by reducing the precision of parameters and store them in less memory , example representing fp32 in fp16 datatype.

Practically speaking this loss of precision wouldn't significantly reduce the LLM output quality but will have significant performance in terms of efficiency.


|                                   | Gemma FP 32 bit precision                                           | Gemma FP16 bit precision                    |
| --------------------------------- | ------------------------------------------------------------------- | ------------------------------------------- |
|                                   |                                                                     | Planck                                      |
| # of Parameters                   | >> model.num_parameters()<br>2,506,172,416<br>                      | >> model.num_parameters()<br>2,506,172,416  |
| Memory Size based on # Parameters | >> model.num_parameters() * 4 / (1024**3)<br>9.336219787597656 GB   | >> model.num_parameters() * 4 / (1024**3)   |
| Memory Footprint                  | >>model.get_memory_footprint()  / (1024**3)<br>9.398719787597656 GB | >>model.get_memory_footprint()  / (1024**3) |
|                                   |                                                                     |                                             |
|                                   |                                                                     |                                             |
|                                   |                                                                     |                                             |




