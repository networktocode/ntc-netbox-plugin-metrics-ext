# Frequently Asked Questions

## NetBox already expose a metrics endpoint, why do I need another one ?

> System metrics and application level metrics are complementary with each other
> - **SYSTEM Metrics** are very useful to instrument code, track ephemeral information and get a better visibility into what is happening. (Example of metrics: nbr of requests, requests per second, nbr of exceptions, response time, etc ...) The idea is that if we have multiple NetBox instances running behind a load balancer each one will produce a different set of metrics and the monitoring system needs to collect these metrics from all running instances and aggregate them in a dashboard. NetBox exposes some system metrics by default at `localhost/metrics`.
> - **APPLICATION Metrics** are at a higher level and represent information that is the same across all instances of an application running behind a load balancer. if I have 3 instances of NetBox running, there is no point to ask each of them how many Device objects I have in the database, since they will always return the same information. In this case, the goal is to expose only 1 endpoint that can be served by any running instance.

## Do I need an API token to access the application metrics endpoint ? 

> No, currently no authentication is required (or possible).

## I don't see the plugin in the API documentation, is it expected ?

> Yes, this is expected. This API endpoint is not published in the swagger documentation because it's not a REST compatible endpoint.

## Does this plugin support NetBox 2.9 ?

> Mostly, everything should work but the reports stats right now. In NetBox 2.9 the way reports are managed internally has changed and the plugin has not been updated yet to support these changes.