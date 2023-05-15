# kubegpt

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/xeol-io/xeol/blob/main/LICENSE)

A command-line tool for using human language to interact with Kubernetes. Powered by OpenAI/GPT.

kubegpt will take your input like

```
kubegpt "Am I using GlusterFS as a storage class?"
```

It will generate a kubectl command to run to get information, read the results of the
command and then interpret the results. It will use your local kubectl config and context
to reach your k8s cluster.

```
kubectl get storageclass
```

An example of the output of the above command is:

```
$ kubegpt "Am I using GlusterFS as a storage class?"

> Entering new AgentExecutor chain...
 I need to use kubectl to query the storage class information.
Action: terminal
Action Input: kubectl get storageclass
Observation: NAME                 PROVISIONER          RECLAIMPOLICY   VOLUMEBINDINGMODE   ALLOWVOLUMEEXPANSION   AGE
hostpath (default)   docker.io/hostpath   Delete          Immediate           false                  14d

Thought: I can see the storage class is "hostpath" which is not GlusterFS.
Final Answer: No, you are not using GlusterFS as a storage class.

> Finished chain.
```

The data you see in `Observation` is _real_ info returned from the kubectl command that the AI agent ran using whatever Kubernetes cluster is currently set in your kubectl context.

## Installation

```
pip install kubegpt
```

Setup your OpenAI API key

```
export OPENAI_API_KEY=xxxx

# NOTE: you will need to add a credit card to the OpenAI dashboard for this to work.
```

And then ask away!

```
kubegpt "What kubernetes context am I using?"
```

## WARNING

Use at your own risk! We tell the OpenAI agent mutliple times to only run non-destructive
kubectl commands but this is not guaranteed. We are not responsible for any damage.
