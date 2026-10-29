# NEST Client -- A client for the NEST Server

The easiest way to interact with the NEST Server is the NEST Client. It can be used either by directly starting a Python
session in a clone of that repository, or by installing it by ```pip``` install therein. NEST Simulator itself does not
have to be installed in order to use the NEST Client.

Using a dynamic function mapping mechanism, the NEST Client supports the same functions as PyNEST does. However, instead
of directly executing calls in NEST, it forwards them together with their arguments to the NEST Server, which in turn
executes them. To you as a user, everything looks much like a typical simulation
code for NEST Simulator.

## Install NEST Client

The client can be installed with this command:

```bash
pip install nest-client
```

## Basic usage

To give you an idea of the usage, the following table shows a comparison of a typical simulation once for PyNEST and
once using the NEST Client identical except for the ```import``` statement:

<table>
<tr>
<td> PyNEST directly </td> <td> via NEST Client </td>
</tr>
<tr>
<td>

```python
import nest

# Reset the kernel
nest.ResetKernel()

# Create nodes
params = {"rate": 6500}
pg = nest.Create("poisson_generator", 1, params)
neurons = nest.Create("iaf_psc_alpha", 1000)
sr = nest.Create("spike_recorder")

# Connect nodes
nest.Connect(pg, neurons, syn_spec={"weight": 10})
nest.Connect(neurons[::10], sr)

# Simulate
nest.Simulate(1000)

# Get events
print("Number of events:", sr.n_events)
```

</td>
<td>

```python
from nest_client import NESTClient

nest = NESTClient()

# Reset the kernel
nest.ResetKernel()

# Create nodes
params = {"rate": 6500}
pg = nest.Create("poisson_generator", 1, params)
neurons = nest.Create("iaf_psc_alpha", 1000)
sr = nest.Create("spike_recorder")

# Connect nodes
nest.Connect(pg, neurons, syn_spec={"weight": 10})
nest.Connect(neurons[::10], sr)

# Simulate
nest.Simulate(1000)

# Get events
n_events = nest.GetStatus(sr, "n_events")
print("Number of events:", n_events)
```
</td>
</tr>
</table>

## Run scripts

The NEST Client is able to send complete simulation scripts to the NEST Server using the functions ```exec_script``` and
```from_file```. The following listing shows a Python snippet using the NEST Server Client to execute a simple script on
the Server using the ```exec_script``` function:

```python
from nest_client import NESTClient
nest = NESTClient()

script = "print('Hello world!')"
response = nest.exec_script(script)
print(response['stdout'])          # 'Hello world!'

script = "models=nest.node_models"
response = nest.exec_script(script, return_vars='models')
models = response['data']
print(models)                      # the list of models
```

In a more realistic scenario, you probably already have your simulation script stored in a file. Such scripts can be
sent to the NEST Server for execution using the ```from_file``` function provided by the NEST Client.

```python
from nest_client import NESTClient

nest = NESTClient()

response = nest.from_file("simulation_script.py", return_vars="n_events")
n_events = response["data"]

print("Number of events:", n_events)
```

> [!NOTE]
>
> By default, the NEST Server only imports the PyNEST module during startup for security reasons. In case you require
> additional Python modules for your simulation script, please see
> [NEST Server](https://github.com/nest/nest-server#security-considerations).


## NEST Client API

| Call | Description |
| ---- | ----------- |
| ```NESTClient``` |  The client object to interact with the NEST Server |
| ```NESTClient.<call>(*args, **kwargs)``` | Execute a PyNEST function ```<call>``` on the NEST Server; the arguments ```args``` and ```kwargs``` will be forwarded to the function |
| ```NESTClient.exec_script(source, return_vars=None)``` | Execute a Python script on the NEST Server; the script has to be given as a string in the ```source``` argument |
| ```NESTClient.from_file(filename, return_vars=None)``` | Execute a Python script on the NEST Server; the argument ```filename``` is the name of the file in which the script is stored |

## Development mode

We recommend to use virtual environment, e.g. with ```uv```:

Install ```nest-client``` as an editable package

```bash
uv pip install -e .
```

### Test against multiple Python versions using ```uv```

```bash
make test-all
```

## References

- [NEST Simulator](http://nest-simulator.org) via its REST-based interface
- [NEST Server](https://nest-simulator.readthedocs.io/en/latest/interface_nest/nest_server.html)
