(function() {

  // Inspired by http://informationandvisualization.de/blog/box-plot
  d3.fbox = function() {
    var boxwidth = 1,
      boxheight = 1,
      duration = 0,
      domain = null,
      value = Number,
      rotate = false,
      showOutliers = true,
      whiskers = boxWhiskers,
      quartiles = boxQuartiles,
      tickFormat = null;

    function boxWidthAxis() {
      return rotate ? "y" : "x";
    }

    function boxHeightAxis() {
      return rotate ? "x" : "y";
    }

    function boxWidthAttrName() {
      return rotate ? "height" : "width";
    }

    function boxHeightAttrName() {
      return rotate ? "width" : "height";
    }

    function boxrange() {
      return rotate ? [0, boxheight] : [boxheight, 5];
    }

    function box(g) {
      g.each(function(d, i) {
        // Gets the label/key for the data to be displayed along with the box
        var k = d.key;
        // Gets hold of the data from inside the server returned json
        d = d.data; 
        d = d.map(value).sort(d3.ascending);
        var g = d3.select(this),
          n = d.length,
          min = d[0],
          max = d[n - 1];

        // Compute quartiles. Must return exactly 3 elements.
        var quartileData = d.quartiles = quartiles(d);

        // Compute whiskers. Must return exactly 2 elements, or null.
        var whiskerIndices = whiskers && whiskers.call(this, d, i),
          whiskerData = whiskerIndices && whiskerIndices.map(function(i) {
            return d[i];
          });
        if (!showOutliers) {
          min = whiskerData[0], max = whiskerData[1];
        }
        // Compute outliers. If no whiskers are specified, all data are "outliers".
        // We compute the outliers as indices, so that we can join across transitions!
        if (showOutliers) {
          var outlierIndices = whiskerIndices ? d3.range(0, whiskerIndices[0]).concat(d3.range(whiskerIndices[1] + 1, n)) : d3.range(n);
          var outlierData = outlierIndices && outlierIndices.map(function(i) {
            return d[i];
          });
        }

        // Compute the new box length-scale.
        var boxHeightScaleNew = d3.scale.linear()
          .domain(domain && domain.call(this, d, i) || [min, max])
          .range(boxrange()); // creating space for the key

        // Retrieve the old x-scale, if this is an update.
        var boxHeightScaleOld = this.__chart__ || boxHeightScaleNew;

        // Stash the new scale.
        this.__chart__ = boxHeightScaleNew;

        var key = g.insert("text")
          .attr("text-anchor", "start")
          .attr("d" + boxWidthAxis(), rotate ? 0 : boxwidth / 3)
          .attr("class", "key").text(k);


        // Note: the box, median, and box tick elements are fixed in number,
        // so we only have to handle enter and update. In contrast, the outliers
        // and other elements are variable, so we need to exit them! Variable
        // elements also fade in and out.

        // Update center line: the vertical line spanning the whiskers.
        var center = g.selectAll("line.center")
          .data(whiskerData ? [whiskerData] : []);

        center.enter().insert("line", "rect")
          .attr("class", "center")
          .attr(boxWidthAxis() + "1", boxwidth / 2)
          .attr(boxHeightAxis() + "1", function(d) {
            return boxHeightScaleOld(d[0]);
          })
          .attr(boxWidthAxis() + "2", boxwidth / 2)
          .attr(boxHeightAxis() + "2", function(d) {
            return boxHeightScaleOld(d[1]);
          })
          .style("opacity", 1e-6)
          .transition()
          .duration(duration)
          .style("opacity", 1)
          .attr(boxHeightAxis() + "1", function(d) {
            return boxHeightScaleNew(d[0]);
          })
          .attr(boxHeightAxis() + "2", function(d) {
            return boxHeightScaleNew(d[1]);
          });

        center.transition()
          .duration(duration)
          .style("opacity", 1)
          .attr(boxHeightAxis() + "1", function(d) {
            return boxHeightScaleNew(d[0]);
          })
          .attr(boxHeightAxis() + "2", function(d) {
            return boxHeightScaleNew(d[1]);
          });

        center.exit().transition()
          .duration(duration)
          .style("opacity", 1e-6)
          .attr(boxHeightAxis() + "1", function(d) {
            return boxHeightScaleNew(d[0]);
          })
          .attr(boxHeightAxis() + "2", function(d) {
            return boxHeightScaleNew(d[1]);
          })
          .remove();



        // Update innerquartile box.
        var box = g.selectAll("rect.box")
          .data([quartileData]);

        box.enter().append("rect")
          .attr("class", "box")
          .attr(boxWidthAxis(), boxwidth / 4)
          .attr(boxHeightAxis(), function(d) {
            console.log(d);
            return rotate ? boxHeightScaleOld(d[0]) : boxHeightScaleOld(d[2]);
          })
          .attr(boxWidthAttrName(), boxwidth / 2)
          .attr(boxHeightAttrName(), function(d) {
            return Math.abs(boxHeightScaleOld(d[0]) - boxHeightScaleOld(d[2]));
          })
          .transition()
          .duration(duration)
          .attr(boxHeightAxis(), function(d) {
            console.log(d);
            return rotate ? boxHeightScaleOld(d[0]) : boxHeightScaleOld(d[2]);
          })
          .attr(boxHeightAttrName(), function(d) {
            return Math.abs(boxHeightScaleNew(d[0]) - boxHeightScaleNew(d[2]));
          });

        // Update median line.
        var medianLine = g.selectAll("line.median")
          .data([quartileData[1]]);

        medianLine.enter().append("line")
          .attr("class", "median")
          .attr(boxWidthAxis() + "1", boxwidth / 4)
          .attr(boxHeightAxis() + "1", boxHeightScaleOld)
          .attr(boxWidthAxis() + "2", 3 * boxwidth / 4)
          .attr(boxHeightAxis() + "2", boxHeightScaleOld)
          .transition()
          .duration(duration)
          .attr(boxHeightAxis() + "1", boxHeightScaleNew)
          .attr(boxHeightAxis() + "2", boxHeightScaleNew);

        // Update whiskers.
        var whisker = g.selectAll("line.whisker")
          .data(whiskerData || []);

        whisker.enter().insert("line", "circle, text")
          .attr("class", "whisker")
          .attr(boxWidthAxis() + "1", boxwidth / 4)
          .attr(boxHeightAxis() + "1", boxHeightScaleOld)
          .attr(boxWidthAxis() + "2", 3 * boxwidth / 4)
          .attr(boxHeightAxis() + "2", boxHeightScaleOld)
          .style("opacity", 1e-6)
          .transition()
          .duration(duration)
          .attr(boxHeightAxis() + "1", boxHeightScaleNew)
          .attr(boxHeightAxis() + "2", boxHeightScaleNew)
          .style("opacity", 1);

        whisker.exit().transition()
          .duration(duration)
          .attr(boxHeightAxis() + "1", boxHeightScaleNew)
          .attr(boxHeightAxis() + "2", boxHeightScaleNew)
          .style("opacity", 1e-6)
          .remove();

        // Update outliers.
        if (showOutliers) {
          var outlier = g.selectAll("circle.outlier")
            .data(outlierIndices, Number);
  
          outlier.enter().insert("circle", "text")
            .attr("class", "outlier")
            .attr("r", 5)
            .attr("c" + boxWidthAxis(), boxwidth / 2)
            .attr("c" + boxHeightAxis(), function(i) {
              return boxHeightScaleOld(d[i]);
            })
            .style("opacity", 1e-6)
            .transition()
            .duration(duration)
            .attr("c" + boxHeightAxis(), function(i) {
              return boxHeightScaleNew(d[i]);
            })
            .style("opacity", 1);
  
          outlier.exit().transition()
            .duration(duration)
            .attr("c" + boxHeightAxis(), function(i) {
              return boxHeightScaleNew(d[i]);
            })
            .style("opacity", 1e-6)
            .remove();
        }

        // Compute the tick format.
        var format = tickFormat || boxHeightScaleNew.tickFormat(8);

        // Update box ticks.
        var boxTick = g.selectAll("text.box")
          .data(quartileData);

        boxTick.enter().append("text")
          .attr("class", "box")
          .attr("d" + boxHeightAxis(), ".3em")
          .attr("d" + boxWidthAxis(), function(d, i) {
            return i & 1 ? 12 : -6;
          })
          .attr(boxWidthAxis(), function(d, i) {
            return i & 1 ? 3 * boxwidth / 4 : boxwidth / 4;
          })
          .attr(boxHeightAxis(), boxHeightScaleOld)
          .attr("text-anchor", function(d, i) {
            return i & 1 ? "start" : "end";
          })
          .text(format)
          .transition()
          .duration(duration)
          .attr(boxHeightAxis(), boxHeightScaleNew);


        // Update whisker ticks. These are handled separately from the box
        // ticks because they may or may not exist, and we want don't want
        // to join box ticks pre-transition with whisker ticks post-.
        var whiskerTick = g.selectAll("text.whisker")
          .data(whiskerData || []);

        whiskerTick.enter().append("text")
          .attr("class", "whisker")
          .attr("d" + boxHeightAxis(), ".3em")
          .attr("d" + boxWidthAxis(), 6)
          .attr(boxWidthAxis(), 3 * boxwidth / 4)
          .attr(boxHeightAxis(), boxHeightScaleOld)
          .text(format)
          .style("opacity", 1e-6)
          .transition()
          .duration(duration)
          .attr(boxHeightAxis(), boxHeightScaleNew)
          .style("opacity", 1);

        whiskerTick.exit().transition()
          .duration(duration)
          .attr(boxHeightAxis(), boxHeightScaleNew)
          .style("opacity", 1e-6)
          .remove();

        // Outlier ticks
        if (showOutliers) {

          var outlierTick = g.selectAll("text.outlier")
            .data(outlierData || []);
  
          outlierTick.enter().append("text")
            .attr("class", "outlier")
            .attr("d" + boxHeightAxis(), ".3em")
            .attr("d" + boxHeightAxis(), ".3em")
            .attr("d" + boxWidthAxis(), 0)
            .attr(boxWidthAxis(), function(d, i) {
              // disperses the tick location better so that they don't overlap
              // really custom stuff :(
              return [2.75,3,7,7.25][i % 4] * (boxwidth / 10); 
            })
            .attr(boxHeightAxis(), boxHeightScaleOld)
            .text(format)
            .style("opacity", 1e-6)
            .transition()
            .duration(duration)
            .attr(boxHeightAxis(), boxHeightScaleNew)
            .style("opacity", 1);
  
          outlierTick.exit().transition()
            .duration(duration)
            .attr(boxHeightAxis(), boxHeightScaleNew)
            .style("opacity", 1e-6)
            .remove();
        }


      });
      d3.timer.flush();
    }

    box.boxwidth = function(x) {
      if (!arguments.length) return boxwidth;
      boxwidth = x;
      return box;
    };

    box.boxheight = function(x) {
      if (!arguments.length) return boxheight;
      boxheight = x;
      return box;
    };

    box.tickFormat = function(x) {
      if (!arguments.length) return tickFormat;
      tickFormat = x;
      return box;
    };

    box.duration = function(x) {
      if (!arguments.length) return duration;
      duration = x;
      return box;
    };

    box.domain = function(x) {
      if (!arguments.length) return domain;
      domain = x == null ? x : d3.functor(x);
      return box;
    };

    box.value = function(x) {
      if (!arguments.length) return value;
      value = x;
      return box;
    };

    box.rotate = function(x) {
      if (!arguments.length) return rotate;
      rotate = x;
      return box;
    };

    box.showOutliers = function(x) {
      if (!arguments.length) return showOutliers;
      showOutliers = x;
      return box;
    };


    box.whiskers = function(x) {
      if (!arguments.length) return whiskers;
      whiskers = x;
      return box;
    };

    box.quartiles = function(x) {
      if (!arguments.length) return quartiles;
      quartiles = x;
      return box;
    };

    return box;
  };

  function boxWhiskers(d) {
    return [0, d.length - 1];
  }

  function boxQuartiles(d) {
    return [
      d3.quantile(d, .25),
      d3.quantile(d, .5),
      d3.quantile(d, .75)
    ];
  }

})();