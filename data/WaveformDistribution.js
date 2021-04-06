function makeResponsive() {

// Define SVG area dimensions
  var svgWidth = 960;
  var svgHeight = 660;

// Define the chart's margins as an object
  var chartMargin = {
    top: 30,
    right: 30,
    bottom: 30,
    left: 40
  };

// Define dimensions of the chart area
  var chartWidth = svgWidth - chartMargin.left - chartMargin.right;
  var chartHeight = svgHeight - chartMargin.top - chartMargin.bottom;

// Select body, append SVG area to it, and set the dimensions
  var svg = d3.select("body")
      .append("svg")
      .attr("height", svgHeight)
      .attr("width", svgWidth);

// Append a group to the SVG area and shift ('translate') it to the right and to the bottom
  var chartGroup = svg.append("g")
      .attr("transform", `translate(${chartMargin.left}, ${chartMargin.top})`);

// Load data from Waveformtotals.csv
  d3.csv("Waveformtotals.csv").then(function (sesData) {

    console.log(sesData);

    // Cast the hours value to a number for each piece of Waveformdata
    sesData.forEach(function (d) {
      d.Count = +d.Count
    });

    // Configure a band scale for the horizontal axis with a padding of 0.1 (10%)
    var xBandScale = d3.scaleBand()
        .domain(sesData.map(d => d.Waveform))
        .range([0, chartWidth])
        .padding(0.1);

    // Create a linear scale for the vertical axis.
    var yLinearScale = d3.scaleLinear()
        .domain([0, d3.max(sesData, d => d.Count)])
        .range([chartHeight, 0]);

    // Create two new functions passing our scales in as arguments
    // These will be used to create the chart's axes
    var bottomAxis = d3.axisBottom(xBandScale);
    var leftAxis = d3.axisLeft(yLinearScale).ticks(8);

    // Append two SVG group elements to the chartGroup area,
    // and create the bottom and left axes inside of them
    chartGroup.append("g")
        .call(leftAxis);

    chartGroup.append("g")
        .attr("transform", `translate(0, ${chartHeight})`)
        .call(bottomAxis);

    // Create one SVG rectangle per piece of Waveformdata
    // Use the linear and band scales to position each rectangle within the chart
    var Rectgroup = chartGroup.selectAll(".bar")
        .data(sesData)
        .enter()
        .append("rect")
        .attr("class", "bar")
        .attr("x", d => xBandScale(d.Waveform))
        .attr("y", d => yLinearScale(d.Count))
        .attr("width", xBandScale.bandwidth())
        .attr("height", d => chartHeight - yLinearScale(d.Count));


    // Append tooltip div
    var toolTip = d3.select("body")
        .append("div")
        .classed("tooltip", true);

    // Create "mouseover" event listener to display tooltip
    Rectgroup.on("mouseover", function (d) {
      toolTip.style("display", "block")
          .html(
              `<strong>Total Waveforms<strong><hr>${d.Count}`)
          .style("left", d3.event.pageX + "px")
          .style("top", d3.event.pageY + "px");
    })
        //  Create "mouseout" event listener to hide tooltip
        .on("mouseout", function () {
          toolTip.style("display", "none");
        });

  }).catch(function (error) {
    console.log(error);
  });
}
// When the browser loads, makeResponsive() is called.
makeResponsive();

// When the browser window is resized, makeResponsive() is called.
d3.select(window).on("resize", makeResponsive)