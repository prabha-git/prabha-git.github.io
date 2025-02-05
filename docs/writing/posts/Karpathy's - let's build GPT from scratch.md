---
draft: false
date: 2024-03-19
slug: lets-build-gpt-from-scratch
tags:
  - llm
authors:
  - Prabha
---
!!!note "Self Note"
	This note is for me to understand the concepts


!!!note "Learning Resource"
	Karpathy's tutorial on Youtube [Lets build GPT from scratch](https://www.youtube.com/watch?v=kCc8FmEb1nY&t=2794s)


## [The spelled-out intro to neural networks and backpropagation: building micrograd - YouTube](https://www.youtube.com/watch?v=VMj-3S1tku0&list=PLAqhIrjkxbuWI23v9cThsA9GvCAUhRvKZ&index=1)

	In this video he buils micrograd


## [The spelled-out intro to language modeling: building makemore - YouTube](https://youtu.be/PaCmpygFfXo?list=PLAqhIrjkxbuWI23v9cThsA9GvCAUhRvKZ)

	Building makemore [GitHub - karpathy/makemore: An autoregressive character-level language model for making more things](https://github.com/karpathy/makemore)

	Dataset: people names dataset in givernment website
	
### Iteration 1:
		Character level language model
		
		Method: Bigram (Predict next char using previous char)
![Pasted%20image%2020250130124540](Pasted%20image%2020250130124540.png)
	As seens above, it doesn't give good names. Bigram model is not good for predicting next character.
	
	In "bigram" model probabilities become the parameter of bigram language model.

### Quality Evaluation of model

We will be using [[Negative maximum log likelihood estimate]] , in our problem we will calculate for the entire training set. 

	Log 1 = 0 & Log (very small number ) = -Inf

We would estimate Negative Log likelihood as follows 

```python
log_likelihood = 0
n = 0
for w in words[:3]:
    chs = ['.'] + list(w) + ['.']
    for ch1, ch2 in zip(chs, chs[1:]):
        ix1 , ix2 = stoi[ch1], stoi[ch2]
        prob=P[ix1, ix2] # P is the matrix that holds the probability
        n+=1
        log_likelihood+=torch.log(prob)
        print(f'{ch1}{ch2}: {prob:.4f}')

print(f'{log_likelihood=}')

#Negative log likelihood give nice property where error (loss function) should be small, i.e zero is good.
nll = -log_likelihood
print(f'{nll=}')

#Usually people work with average negative log likelihood
print(f'{nll/n=}')
```
	

To avoid infinity probability for some predictions, people do model "smoothing" (assigning very small probability to unlikely scenario)

### Iteration 2: Bigram Language Model using Neural Network

Need to create a dataset for training, i.e input and output char pair. (x and y).

One hot encoding needs to be done before feeding into NN

`Log {count} = Logits`
`counts = exp(Logits)`

```python

xenc = F.one_hot(xs, num_classes = 27).float()
for i in range(100):
    
    # Forward Pass
    logits = xenc @ W # Pred log-counts
    
    counts = logits.exp() # Counts
    
    probs = counts  / counts.sum(1, keepdims = True) 
    
    loss = -probs[torch.arange(228146), ys].log().mean()
    print(loss.item())

    #Backward pass
    W.grad=None
    loss.backward()

    #Update parameters using the gradient calculated
    W.data+= -50  * W.grad # here 50 is h , initial tried small numbers , like 0.1 but it is decreasing the loss very slowly hence increased to 50

    
    
```


### Thoughts and comparison of above two approaches

In the first approach, we added 1 to the actual count because we don't want to end up in a situation it give $-\infty$ for the character pair it didn't see in the trainin dataset. If you add large number then actual frequency is less relevent and we get uniform distribution. It is called smoothing


Similarly, gradient based approach has a way to "smoothing". When you keep all values of `W` to be zero, exp(W) gives all ones and softmax would provide equal probabilities to all outputs. You incentivise this in loss function by using second component like below 

 ```
loss = -probs[torch.arange(228146), ys].log().mean() + (0.1 * (W**2).mean())
```

Second component pushed W to be zero , 0.1 is the strength of Regularization that determines the how much weight we want to give to this regularization component. It is similar to the number of "fake" count you add in the first approach.

We took two approaches 

i)  Frequency based model 
ii) NN based model (using Negative log likelihood to optimize)

We ended up with the same model , in the  NN based approach the `W` represents the log probability (same as first approach) , we can exponential the `W` to get count 



## [Building makemore Part 2: MLP - YouTube](https://www.youtube.com/watch?v=TCH_1BHY58I)

In this class we would build makemore to predict based on last 3 characters.

#### Embedding
As a first step, we need to build embedding for the characters, we start with 2 dimensional embedding.

![[Pasted image 20250205123847.png]]

```python
h = emb.view(-1, 6) @ W1 + b1 # Hiden layer activation
```

We index on embedding matrix to get the weight / embeddings for the character. Another way to interpret is one hot encoding. indexing and one hot encoding produce similar result. in this case we think first layer as weight of neural network.

```python
logits = h @ W2 + b2
counts = logits.exp()
prob = counts/counts.sum(1,keepdims=True)
prob.shape
# torch.Size([32, 27])
```

In Final layer we get probability distribution for all 27 characters.


```python
# Negative Log likelihood 

loss = -prob[torch.arange(32), Y].log().mean()
loss
```

In Practice, we use mini batch for forward or backward pass. it is efficient than optimizing on the entire dataset.

it is much efficient to take many steps (iteration) with low confidence in gradient

#### Learning rate

Learning rate is an important hyper , we need to find the reasonable range manually and we can use different techniques to search for the optimal parameter in that range.

#### Dataset split

Important to split dataset into three sets
 - train split is to find model parameters 

- dev split is to find hyper parameters

- test split is to evaluate the model performance finally

we improve the model by increasing the complexity by increasing the parameters. for example hidden layer neurons can be increased.


In our case , bottle neck may be the embeddings, we are cramping all the character in just two dimensional space. we can increase embedding dimensions to 10 from 2.

Now we get better name sounding words than before ( with just one character in context)

```
dex.
marial.
mekiophity.
nevonimitta.
nolla.
kyman.
arreyzyne.
javer.
gota.
mic.
jenna.
osie.
tedo.
kaley.
mess.
suhaiaviyny.
fobs.
mhiriel.
vorreys.
dasdro.
```

