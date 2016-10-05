## Decisions
From this point (5-Oct-2016), all significant decisions on design or tool choice will be documented here for reference for anybody involved in the project. Earlier choices might eventually get added if possible

#### 5-Oct-2016

##### Perf Testing tool choice
Settled on locust io since it seems ok and is in python. Gatling has better reporting but then I need a scala setup. So locust wins over. Also locust gives basic percentile data which is reasonable for me. Later point in time we will figure out if we can integrate locust with graphite/grafana
