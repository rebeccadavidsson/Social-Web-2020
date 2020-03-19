// Annemijn Dijkhuis 11149272
// Eindproject Minor programmeren
// Maakt en update een staafdiagram

// margins van SVG
var marginBar = {top: 40, right: 100, bottom: 30, left: 40}
var widthBar = 1100 - marginBar.left - marginBar.right
var heightBar = 300 - marginBar.top - marginBar.bottom

// tooltips van bar
var tipBar =  d3.tip()
              .attr("class", "d3-tip")
              .offset([-10, 0])
              .html(function(d) {
                return "<strong>" + d.key + "</strong><span class='details'>" +
                "<br></span>" +

                "Aantal studenten: <span class='details'>" +
                d.value+"</span>" + "<br>"+
                "Klik om te verwijderen";
              })

function barGraph(){
  // maakt een bargraph, returnt 0 als er iets mis gaat

  // maakt SVG
  var svg = d3.select("#barGraph svg")
              .attr("width", widthBar + marginBar.left + marginBar.right)
              .attr("height", heightBar + marginBar.top + marginBar.bottom)


  var  g = svg.append("g")
              .attr("transform", "translate(" + marginBar.left + "," +
               marginBar.top + ")");


  var title = d3.select("#barGraph svg")
                .append("text")
                .text("Aantal eerstejaarsaanmeldingen in het WO verschillend tussen man en vrouw")
                .attr("x", function() {return widthBar/3})
                .attr("y", function() {return marginBar.bottom/2})


  // schaal voor het maken van de bargroups
  var x0 = d3.scaleBand()
      .rangeRound([0, widthBar])
      .paddingInner(0.1);

  // schaal voor de bars zelf
  var x1 = d3.scaleBand()
      .padding(0.05);

  // yschaal
  var y = d3.scaleLinear()
      .rangeRound([heightBar, 0]);

  // kleurenschaal
  var z = d3.scaleOrdinal()
        .range(d3.schemeDark2)

  // de variabelen
  var keys = ["Vrouw", "Man", "Totaal"]

  // make een default bargraph
  updateBarGraph("Biomedische Wetenschappen", "Universiteit van Amsterdam", 2016, "Append")


  x0.domain(BARGRAPHDATA.map(function(d) { return `${d.Opleiding}, ${d.Instelling}, ${d.jaar}`; }));
  x1.domain(keys).rangeRound([0, x0.bandwidth()]);
  y.domain([0, d3.max(BARGRAPHDATA, function(d) { return d3.max(keys, function(key) { return d[key]; }); })]).nice();

  // maak een xas
  g.append("g")
      .attr("class", "xAxisBar")
      .attr("transform", "translate(0," + heightBar   + ")")
      .call(d3.axisBottom(x0));

  // maak een y as
  g.append("g")
      .attr("class", "yAxisBar")
      .call(d3.axisLeft(y).ticks(null, "s"))
    .append("text")
      .attr("x", 2)
      .attr("y", y(y.ticks().pop()) + 0.5)
      .attr("dy", "0.32em")
      .attr("fill", "#000")
      .attr("font-weight", "bold")
      .attr("text-anchor", "start")
      .text("Aantal studenten");


  // maak een legenda
  var legend = svg.append("g")
      .attr("transform", function(d) {return "translate(20,0)"})
      .attr("font-family", "sans-serif")
      .attr("font-size", 10)
      .attr("text-anchor", "end")
    .selectAll("g")
    .data(keys.slice())
    .enter().append("g")
      .attr("transform", function(d, i) {  return "translate(0," + i * 20 + ")"; });

  legend.append("rect")
      .attr("x", widthBar + marginBar.right)
      .attr("width", 15)
      .attr("height", 15)
      .attr("fill", z)
      .attr("stroke", z)
      .attr("stroke-width",2)

  legend.append("text")
      .attr("x", widthBar + marginBar.right - 7)
      .attr("y", 9.5)
      .attr("dy", "0.32em")
      .text(function(d) { return d; });

}

  function updateBarGraph(opleiding, instelling, jaar, type) {
    // update een bargraph

    // verberg de alert
    $(".alert").hide()

    // definieer de SVG
    var svg = d3.select("#barGraph svg")

    // call tip
    svg.call(tipBar);

    // vind de juiste dataset

    // als "Alles" is aangekruisd
    if (opleiding === "Alles"){

      UNIDATA.forEach(function(d){
        if (d["INSTELLINGSNAAM ACTUEEL"] === instelling){
          var vrouwen = parseInt((d[`${jaar} VROUW`]));
          var mannen = parseInt((d[`${jaar} MAN`]));
          var totaal = parseInt((d[`TOTAAL ${jaar}`]));

          if (totaal == 0){

            // als er geen studenten waren, laat alert zien
            $("#alert").text("Geen studenten");
            $("#alert").show();
            return 0;
          }

          // controleer de bedoeling van de gebruiker
          for (var i = 0; i < BARGRAPHDATA.length; i++){
            if (opleiding === BARGRAPHDATA[i]["Opleiding"]){
              if (instelling === BARGRAPHDATA[i]["Instelling"]){
                if (jaar === BARGRAPHDATA[i]["jaar"]){
                  if (type === "Delete"){
                  BARGRAPHDATA.splice(i, 1);
                  }
                  else{

                    // deze data is al ingebruik
                    return 0;
                  };
                };
              };
            };
          };

          // controleert of de data mag worden gebruikt
          if (type === "Append"){
            if (BARGRAPHDATA.length > 3){

                // alert de gebruiker bij te veel data
                $("#alert").text(MESSAGE)
                $(".alert").show()
            }
            else{
                BARGRAPHDATA.push({Instelling: instelling, Opleiding: opleiding,
                    jaar:jaar, Man: mannen, Vrouw: vrouwen, Totaal: totaal})
            };
          };
        };
      });
    }

    // als een opleiding is aangeklikt
    else{
      ALLDATA.forEach(function(d){
        if (d["INSTELLINGSNAAM ACTUEEL"] === instelling){
          if (d["OPLEIDINGSNAAM ACTUEEL"] === opleiding){
            var vrouwen = parseInt((d[`${jaar} VROUW`]));
            var mannen = parseInt((d[`${jaar} MAN`]));
            var totaal = mannen + vrouwen;

            if (totaal == 0){

              // als 0, geeft alert
              $("#alert").text("Geen studenten");
              $("#alert").show();
              return 0;
            }

            // contorleert of de data mag worden gebruikt
            for (var i = 0; i < BARGRAPHDATA.length; i++){
              if (opleiding === BARGRAPHDATA[i]["Opleiding"]){
                if (instelling === BARGRAPHDATA[i]["Instelling"]){
                  if (jaar === BARGRAPHDATA[i]["jaar"]){
                    if (type === "Delete"){
                      BARGRAPHDATA.splice(i, 1);
                    }
                    else{
                      // data is al in de dataset
                      return 0;
                    }
                  }
                }
              }
            }

          // alert als er teveel datasets zijn
          if (type === "Append"){
            if (BARGRAPHDATA.length > 3){
                $("#alert").text(MESSAGE)
                $(".alert").show()
              }
              else{
                BARGRAPHDATA.push({Instelling: instelling, Opleiding: opleiding,
                  jaar:jaar, Man: mannen, Vrouw: vrouwen, Totaal: totaal})
              };
            };
          };
        };
      });
    };

    var data = BARGRAPHDATA;

    var svg = d3.select("#barGraph svg");

    // get the keys that are needed to get the data
    var keys = ["Vrouw", "Man", "Totaal"];

    // make scales for the axes
    var x0 = d3.scaleBand()
              .rangeRound([0, widthBar])
              .paddingInner(0.1);

    var x1 = d3.scaleBand()
              .padding(0.05);

    var y = d3.scaleLinear()
              .rangeRound([heightBar, 0]);


    var z = d3.scaleOrdinal()
              .range(d3.schemeDark2);

    x0.domain(data.map(function(d) { return `${d.Opleiding}, ${d.Instelling}, ${d.jaar}`; }));
    x1.domain(keys).rangeRound([0, x0.bandwidth()]);
    y.domain([0, d3.max(data, function(d) { return d3.max(keys, function(key) { return d[key]; }); })]).nice();


    // update the x axis
    d3.select(".xAxisBar")
      .transition()
      .duration(500)
      .call(d3.axisBottom(x0))
      .selectAll("text")
      .style("font-size", "7px");

    // update the y axis
    d3.select(".yAxisBar")
      .transition()
      .call(d3.axisLeft(y).ticks(null, "s"))
      .duration(500);


    var dataKeys = [];

   data.forEach(function(d){
     return keys.map(function(key) {
        return dataKeys.push({key: key, value: d[key]});
      });
    });

    // remove necessary groups
    var groups = svg.selectAll(".bar").data(data);

    groups.exit().remove();

    // update the groups
    groups
    .transition()
    .duration(100)
    .attr("transform", function(d) {
      return "translate(" + x0(`${d.Opleiding}, ${d.Instelling}, ${d.jaar}`)
      + ")"; });

    // update the newly inserted groups
    d3.selectAll("#extra")
      .transition()
      .duration(100)
      .attr("transform", function(d) {
        return "translate(" + (x0(`${d.Opleiding}, ${d.Instelling}, ${d.jaar}`) +
        marginBar.left) + "," + marginBar.top + ")";
      });


    // enter the new groups and rectangles
    groups
      .enter()
      .append("g")
      .attr("class","bar")
      .attr("id", "extra")
      .attr("transform", function(d) {
        return "translate(" + (x0(`${d.Opleiding}, ${d.Instelling}, ${d.jaar}`) +
         marginBar.left)  + "," + marginBar.top + ")";
       })
      .on("click",function(d) {
          updateBarGraph(d.Opleiding,
                          d.Instelling, d.jaar, "Delete");
          })
      // enter the rectangles
      .selectAll("rect")
      .data(function(d) {return keys.map(function(key) { return {key: key, value: d[key]}; }); })
      .enter().append("rect")
        .on("mouseover", function(d){

          // show tooltip
          tipBar.show(d);

        })
        .on("mouseout", function(d){

          // hide tooltip
          tipBar.hide(d);
        })
        .on("click", function(d){

          // hide tooltip
          tipBar.hide(d);
        })
        .attr("class", "barRect")
        .attr("y", function(d) { return y(0); })
        .attr("height", "0")
        .attr("width", function(d) {
          return x1.bandwidth();
        })
        .transition()
        .duration(100)
        .attr("y", function(d){
              return y(d.value);
            })
        .attr("height", function(d){
          return heightBar - y(d.value);
        })
        .attr("fill", function(d) { return z(d.key); })
        .attr("x", function(d) { return x1(d.key); })

    // check bar data
    var bars = svg.selectAll(".bar").selectAll("rect")
      .data(function(d) { return keys.map(function(key) {
        return {key: key, value: d[key]}; }); })

    // Adjust the remaining bars
    bars
      .transition()
      .attr("x", function(d) { return x1(d.key); })
      .attr("y", function(d, i) { return y(d.value); })
      .attr("height", function(d, i) {
          return heightBar - y(d.value);
        })
      .attr("width", x1.bandwidth())
      .attr("fill", function(d) {return z(d.key); })
      .duration(500);
  }
