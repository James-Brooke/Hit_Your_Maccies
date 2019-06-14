
    // set the dimensions and margins of the graph
    var margin = {top: 20, right: 20, bottom: 400, left: 40},
        width = 1200 - margin.left - margin.right,
        height = 700 - margin.top - margin.bottom;

    // append the svg object to the body of the page
    // append a 'group' element to 'svg'
    // moves the 'group' element to the top left margin
    var svg = d3.select("#GraphHolder").append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .attr("class", "border rounded")
        .style("background-color", 'White')
        .append("g")
        .attr("transform", 
            "translate(" + margin.left + "," + margin.top + ")");

    function drawGraph(data, redraw=false) {

        // remove previous bars / axes
        if (redraw){
            svg.selectAll(".bar").remove();
            svg.selectAll('.yaxis').remove();
            svg.selectAll('.xaxis').remove();
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
            .padding(0.1);
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
        var xAxis = d3.axisBottom(x);
        var yAxis = d3.axisLeft(y);

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
            .on("mouseover", function(d) {
                d3.select(this)
                .style("fill", "red");
                tooltip.transition()		
                    .duration(200)		
                    .style("opacity", .9);
                tooltip .html(d.fields.name + "<br/>" + d.fields.cal + " calories" + "<br/>" + d.fields.pro + "g protein")	
                .style("left", (d3.event.pageX) + "px")		
                .style("top", (d3.event.pageY - 28) + "px")
            })         
            .on("mouseout", function(d) {
                d3.select(this)
                .style("fill", "black");
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