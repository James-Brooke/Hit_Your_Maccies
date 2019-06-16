// set the dimensions and margins of the graph
var margin = {top: 20, right: 20, bottom: 400, left: 60},
    width = 1200 - margin.left - margin.right,
    height = 750 - margin.top - margin.bottom;

// append the svg object to the body of the page
var svg = d3.select("#GraphHolder").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .style("background-color", 'Gainsboro')
    .style("border", "1px solid black")
    .style("border-radius", ".25rem")
    // append a 'group' element to 'svg'
    .append("g")
    .attr("id", "Graph")
    // moves the 'group' element to the top left margin
    .attr("transform", 
        "translate(" + margin.left + "," + margin.top + ")");

function drawGraph(data, redraw=false) {

    // remove previous bars / axes
    if (redraw){
        svg.selectAll('.bar').remove();
        svg.selectAll('.yaxis').remove();
        svg.selectAll('.xaxis').remove();
        svg.selectAll('.grid').remove();            
        svg.selectAll('.label').remove();
    };

    // get values from dropdowns
    var category = document.getElementById("id_category").value;
    var macro = document.getElementById("id_macro").value;

    // filter on category
    data = data.filter(function(d) {return d.fields.category === category;})

    // remove data with 0 macro to prevent empty bars
    if (macro == 'pro'){
        data = data.filter(function(d) {return d.fields.pro > 0})
    } else {
        data = data.filter(function(d) {return d.fields.cal > 0})
    };

    // Sort data by macro choice
    if (macro == 'pro'){
        data = data.sort(function(x, y){
            return d3.descending(x.fields.pro, y.fields.pro)
        });
    } else {
        data = data.sort(function(x, y){
            return d3.descending(x.fields.cal, y.fields.cal)
        });
    };

    // define the ranges
    var x = d3.scaleBand()
        .range([0, width])
        .paddingInner(0.1);
    var y = d3.scaleLinear()
        .range([height, 0]);

    // scale the range for the axes with respect to data
    x.domain(data.map(function(d) { return d.fields.name; }));
    if (macro==='cal'){
        y.domain([0, d3.max(data, function(d) { return d.fields.cal; })]);
    } else{
        y.domain([0, d3.max(data, function(d) { return d.fields.pro; })]);
    };

    // define the axes
    var xAxis = d3.axisBottom(x).tickSizeOuter(0);
    var yAxis = d3.axisLeft(y).tickSizeOuter(0);
    
    // add the axes
    svg.append("g")
        .attr("class", "xaxis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis)
        .selectAll('text')
        .attr("y", -3) // position labels
        .attr("x", 9)
        .attr("transform", "rotate(90)")
        .style("text-anchor", "start");
    svg.append("g")
        .attr("class", "yaxis")
        .call(yAxis);

    // add a grid to the y axis    
    svg.append("g")
        .attr("class", "grid")
        .call(d3.axisLeft(y)
                .tickSize(-width)
                .tickFormat("")
                .tickSizeOuter(0)
        );

    // draw box around plot
    svg.append("line")
        .attr("class", "plot_border")
        .attr("x1", 0)
        .attr("y1", 0)
        .attr("x2", width)
        .attr("y2", 0);
    svg.append("line")
        .attr("class", "plot_border")
        .attr("x1", width)
        .attr("y1", 0)
        .attr("x2", width)
        .attr("y2", height);

    // add label for the x axis
    var graph_height = d3.select("#Graph").node().getBBox().height;
    svg.append("text")             
        .attr("transform",
                "translate(" + (width/2) + " ," + 
                    (graph_height + 20) + ")")
        .style("text-anchor", "middle")
        .attr("class", "label")
        .text("Food")
        .style("font-weight", "bold");      

    
    var macro_mapping = {
        "pro": "Protein (g)",
        "cal": "Calories"
    };
        // text label for the y axis
    svg.append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 0 - margin.left)
        .attr("x",0 - (height / 2))
        .attr("dy", "1em")
        .attr("class", "label")
        .style("text-anchor", "middle")
        .text(macro_mapping[macro])
        .style("font-weight", "bold");      

    // Define the div for the tooltip
    var tooltip = d3.select("#GraphHolder").append("div")	
        .attr("class", "tooltip")				
        .style("opacity", 0);
    
    // append the rectangles for the bar chart
    svg.selectAll(".bar")
        .data(data)
        .enter().append("rect")
        .attr("class", "bar")
        .attr("x", function(d) { return x(d.fields.name); })
        .attr("width", x.bandwidth())
        .style("fill", "#ffc300")
        .style("stroke", "black")
        // define mouseover effects
        .on("mouseover", function(d) {
            d3.select(this)
                .style("fill", "#dd1021");
            svg.append("line")
                .style("stroke", "#dd1021")
                .style("stroke-width", 2)
                .attr("class", "hover_line")
                .attr("x1", 0)
                .attr("y1", height - this.height.baseVal.value)
                .attr("x2", width)
                .attr("y2", height - this.height.baseVal.value);
            tooltip.transition()		
                .duration(200)		
                .style("opacity", .9);
            tooltip.html("<b>" + d.fields.name + "</b>" + "<br>" + d.fields.cal + 
                    " calories" + "<br>" + d.fields.pro + "g protein")	
                .style("left", (d3.event.pageX) + "px")		
                .style("top", (d3.event.pageY - 60) + "px")
        })         
        .on("mouseout", function(d) {
            d3.select(this)
                .style("fill", "#ffc300");
            svg.selectAll('.hover_line').remove();
            tooltip.transition()		
                .duration(500)		
                .style("opacity", 0);	
        });

    if (macro==='cal'){
        svg.selectAll(".bar")
            .attr("y", function(d) { return y(d.fields.cal); })
            .attr("height", function(d) { return height - y(d.fields.cal); })
        } else {
            svg.selectAll(".bar")
            .attr("y", function(d) { return y(d.fields.pro); })
            .attr("height", function(d) { return height - y(d.fields.pro); })
        }

    };

d3.json("/data", function(error, data) {
    if (error) {
        throw error;
    };

    drawGraph(data);

    // add a change event handler to dropdowns
    d3.selectAll("#id_category, #id_macro").on("change", function() {
        drawGraph(data, redraw=true);
        });
});
