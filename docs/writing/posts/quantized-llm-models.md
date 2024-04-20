---
draft: false
date: 2024-04-19
slug: quantized-llm-models
tags:
  - llm
authors:
  - Prabha
---

# Quantized LLM Models

Large Language Models (LLMs) are known for their vast number of parameters, often reaching billions. For example, open-source models like Llama2 come in sizes of 7B, 13B, and 70B parameters, while Google's Gemma has 2B parameters. Although OpenAI's GPT-4 architecture is not publicly shared, it is speculated to have more than a trillion parameters, with 8 models working together in a mixture of experts approach.

## Understanding Parameters

A parameter is a model weight learned during the training phase. The number of parameters can be a rough indicator of a model's capability and complexity. These parameters are used in huge matrix multiplications across each layer until an output is produced.

## The Problem with LLMs

As LLMs have billions of parameters, loading all the parameters into memory and performing massive matrix multiplications becomes a challenge. Let's consider the math behind this:

For a 70B parameter model (like the Llama2-70B model), the default size in which these parameters are stored is 32 bits (4 bytes). To load this model, you would need:

70B parameters * 4 bytes = 260 GB of memory

This highlights the significant memory requirements for running LLMs.

## Quantization as a Solution

Quantization is a technique used to reduce the size of the model by decreasing the precision of parameters and storing them in less memory. For example, representing 32-bit floating-point (FP32) parameters in a 16-bit floating-point (FP16) datatype.

In practice, this loss of precision does not significantly degrade the output quality of LLMs but offers substantial performance improvements in terms of efficiency. By quantizing the model, the memory footprint can be reduced, making it more feasible to run LLMs on resource-constrained systems.

Quantization allows for a trade-off between model size and performance, enabling the deployment of LLMs in a wider range of applications and devices. It is an essential technique for making LLMs more accessible and efficient while maintaining their impressive capabilities.



|                                   | Gemma FP 32 bit precision                                           | Gemma FP16 bit precision                                          |
| --------------------------------- | ------------------------------------------------------------------- | ----------------------------------------------------------------- |
|                                   |                                                                     | Planck                                                            |
| # of Parameters                   | >> model.num_parameters()<br>2,506,172,416<br>                      | >> model.num_parameters()<br>2,506,172,416                        |
| Memory Size based on # Parameters | >> model.num_parameters() * 4 / (1024**3)<br>9.336219787597656 GB   | >> model.num_parameters() * 4 / (1024**3)<br>4.668109893798828 GB |
| Memory Footprint                  | >>model.get_memory_footprint()  / (1024**3)<br>9.398719787597656 GB | >>model.get_memory_footprint()  / (1024**3)<br>4.730609893798828  |
| Average Inference time            | 10.36 seconds                                                       | 7.48 seconds                                                      |
| Distribution of                   | ![[Pasted image 20240420104243.png]]                                | ![[Pasted image 20240420104320.png]]                              |
|                                   |                                                                     |                                                                   |

it is 28% faster with ~50% less memory.

How about accuracy? 

I ran the output of both the models and computed similarity score using OpenAIs `text-embedding-3-large` and got the similarity score.


