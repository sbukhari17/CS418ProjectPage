var jsonObjects = [];
var dict = {};
$(document).ready( function() {
  $.getJSON("json/query_6.json", function(data){
    let rest_list = data.Restaurants;
    var comboBox = $('#combobox');
    for(i=0; i<rest_list.length; i++){
        // jsonObjects.push(rest_list[i]);
        comboBox.append('<option value="' + rest_list[i].Name + '">' + rest_list[i].Name + '</option>');
    }
  });
  $.getJSON("json/query_5.json", function(data){
    let rev_list = data.Reviews;
    for(i=0; i<rev_list.length; i++){
      var rName = rev_list[i]["Restaurant Name"];
      var sent = rev_list[i]["Sentiment labels"];
      var rating = rev_list[i]["Review Rating"];
       if(!(rName in dict)){
         var sent_list = [sent];
         var rating_list = [rating];
         var obj = {
           sent_list, rating_list
         };
         dict[rName] = obj;
       }
       else{
         var obj = dict[rName];
         var sent_list = obj.sent_list;
         var rating_list = obj.rating_list;
         obj.sent_list.push(sent);
         obj.rating_list.push(rating);
         dict[rName] = {sent_list, rating_list};
       }
      jsonObjects.push(rev_list[i]);
    }
  });
  $('#plotButton').click(function(){
    val = $('#inputBox').val();
    if(val in dict){
      var obj = dict[val];
      var sent_list = obj.sent_list;
      var rating_list = obj.rating_list;
      var pos_rating_list = [];
      var pos_id_list = [];
      var neg_rating_list = [];
      var neg_id_list = [];

      for(i=0; i< sent_list.length; i++){
        if(sent_list[i] == "pos"){
          pos_rating_list.push(rating_list[i]);
          pos_id_list.push(i+1);
        }
        else{
          neg_rating_list.push(rating_list[i]);
          neg_id_list.push(i+1);
        }
      }

      var trace1 = {
    x: pos_id_list,
    y: pos_rating_list,
    mode: 'markers',
    type: 'scatter',
    name: 'Positive',
    textposition: 'top center',
    textfont: {
      family:  'Raleway, sans-serif'
    },
    marker: { size: 12,
    color: '#00DE00' }
  };


var trace2 = {
x: neg_id_list,
y: neg_rating_list,
mode: 'markers',
type: 'scatter',
name: 'Negative',
textfont : {
  family:'Times New Roman'
},
textposition: 'bottom center',
marker: { size: 12,
color:'#DE0000' }
};

var data = [ trace1, trace2 ];

var layout = {
xaxis: {
  title: 'Review Number'
},
yaxis: {
  title:'Rating'
},
legend: {
  y: 0.5,
  yref: 'paper',
  font: {
    family: 'Arial, sans-serif',
    size: 20,
    color: 'grey',
  }
},
title:val
};

Plotly.newPlot('tester', data, layout);
    }
  });
  $.widget( "custom.combobox", {
    _create: function() {
      this.wrapper = $( "<span>" )
        .addClass( "custom-combobox" )
        .insertAfter( this.element );

      this.element.hide();
      this._createAutocomplete();
      this._createShowAllButton();
    },

    _createAutocomplete: function() {
      var selected = this.element.children( ":selected" ),
        value = selected.val() ? selected.text() : "";

      this.input = $( "<input>" )
        .appendTo( this.wrapper )
        .val( value )
        .attr( "title", "" )
        .attr('id', 'inputBox')
        .addClass( "custom-combobox-input ui-widget ui-widget-content ui-state-default ui-corner-left" )
        .autocomplete({
          delay: 0,
          minLength: 0,
          source: $.proxy( this, "_source" )
        })
        .tooltip({
          classes: {
            "ui-tooltip": "ui-state-highlight"
          }
        });

      this._on( this.input, {
        autocompleteselect: function( event, ui ) {
          ui.item.option.selected = true;
          this._trigger( "select", event, {
            item: ui.item.option
          });
        },

        autocompletechange: "_removeIfInvalid"
      });
    },

    _createShowAllButton: function() {
      var input = this.input,
        wasOpen = false;

      $( "<a>" )
        .attr( "tabIndex", -1 )
        .attr( "title", "Show All Items" )
        .tooltip()
        .appendTo( this.wrapper )
        .button({
          icons: {
            primary: "ui-icon-triangle-1-s"
          },
          text: false
        })
        .removeClass( "ui-corner-all" )
        .addClass( "custom-combobox-toggle ui-corner-right" )
        .on( "mousedown", function() {
          wasOpen = input.autocomplete( "widget" ).is( ":visible" );
        })
        .on( "click", function() {
          input.trigger( "focus" );

          // Close if already visible
          if ( wasOpen ) {
            return;
          }

          // Pass empty string as value to search for, displaying all results
          input.autocomplete( "search", "" );
        });
    },

    _source: function( request, response ) {
      var matcher = new RegExp( $.ui.autocomplete.escapeRegex(request.term), "i" );
      response( this.element.children( "option" ).map(function() {
        var text = $( this ).text();
        if ( this.value && ( !request.term || matcher.test(text) ) )
          return {
            label: text,
            value: text,
            option: this
          };
      }) );
    },

    _removeIfInvalid: function( event, ui ) {

      // Selected an item, nothing to do
      if ( ui.item ) {
        return;
      }

      // Search for a match (case-insensitive)
      var value = this.input.val(),
        valueLowerCase = value.toLowerCase(),
        valid = false;
      this.element.children( "option" ).each(function() {
        if ( $( this ).text().toLowerCase() === valueLowerCase ) {
          this.selected = valid = true;
          return false;
        }
      });

      // Found a match, nothing to do
      if ( valid ) {
        return;
      }

      // Remove invalid value
      this.input
        .val( "" )
        .attr( "title", value + " didn't match any item" )
        .tooltip( "open" );
      this.element.val( "" );
      this._delay(function() {
        this.input.tooltip( "close" ).attr( "title", "" );
      }, 2500 );
      this.input.autocomplete( "instance" ).term = "";
    },

    _destroy: function() {
      this.wrapper.remove();
      this.element.show();
    }
  });

  $( "#combobox" ).combobox();
} );
