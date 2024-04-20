
- LLM model is getting bigger, quantization helps reduce model size with little to no quality degradation
- ![[Pasted image 20240415112817.png]]

- Some state of art methods to reduce models are 
	- Pruning
		- Removing layers which do not contribute to model decisions
	- Knowledge Distillation
		- Train a student model using the teacher model, 
		- Challenge is you still need to fit original large model in your machine
	- Quantization
		- in nn you can quantize weights, activations
		- Idea is to represent model weights with lower precision (achieved by converting to different dtype )