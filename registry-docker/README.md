# Converting Patient Registry into df for DB entry

+ python code is ready as `import registry`
    * registry.get_sample_df() converts excel sheets into sample_dfs

+ store your own code in `<mounted_volume>/code` and import directly (is added to PYTHONPATH)

+ nb_templates contains exemplary notebooks for correct usage

+ run with `docker run -p <local-IP>:8888 -v $(pwd):/home/martin/work martin37szyska/registry:<TAG>`



### Based on Jupyter Docker Stacks with modifications focused on size and simplicity

visit their documentation for more great content
* [Jupyter Docker Stacks on ReadTheDocs](http://jupyter-docker-stacks.readthedocs.io/en/latest/index.html)

Alpine versions are also available based on [alpine-miniconda3](https://hub.docker.com/r/frolvlad/alpine-miniconda3) with even smaller size

+ build the alpine version with:
    * `--build-arg=latest-alpine --build-arg=CURRENTUSER=10151`