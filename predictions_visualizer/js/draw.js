function drawPlayers(){
	var markup = '<tr>';
	for(name in predictions) {
		markup += '<td id=\"' + name + '\">' + name + '</td>';
	}
	markup += '<td id=\"agg\">Aggregate</td></tr>';
	$('#players').append(markup);
}

function drawAggregateData(){
	for(name in predictions) {
		var list = drawDeckProbabilities(name);
		$('#' + name + '-table').append(list);
	}
}

function drawPlayerData(event) {
	$('#predictions').empty();
	$('#player-details').empty();
	
	if(event['target'].id == "agg") {
		$('#predictions-container').hide();
		$('#player-data-overlay-container').hide();
		drawAggregateData();
		$('#aggregate-container').show();
	} else {
		$('#aggregate-container').hide();
		var name = event['target'].id;
		var markup = drawDeckProbabilities(name);
		$('#predictions').append(markup)
		$('#predictions-container').show();
		$('#player-data-overlay-container').show();
	}
}

function drawDeckProbabilities(name){
	var predictions_array = Object.keys(predictions[name]).map(function(key) {
		return [key, predictions[name][key]];
	});

	predictions_array.sort(function(a, b) {
		return b[1]['percent'] - a[1]['percent'];
	});
	var markup = "";
	for(var i = 0; i < predictions_array.length; i++) {
		if(i>11) { break; }
		
		var pct = Math.round((predictions_array[i][1]['percent'] * 100));
		var name = predictions_array[i][0];
		name = name.replace(".txt", "");
		markup = markup + '<tr><td class=\"decklist\" id=\"' + i + '\">' + name + ' ' + pct + '%</td></tr>';
	}
	return markup;
}

function drawPlayerDetails(event, active_player) {
	$('#player-details').empty();
	var index = event['target'].id
	var predictions_array = Object.keys(predictions[active_player]).map(function(key) {
		return [key, predictions[active_player][key]];
	});

	var markup = "";
	decklist = predictions_array[index][1]['list'];

	for(var c = 0; c < decklist.length; c++ ) {
		c_name = decklist[c]['name'];
		c_copies = decklist[c]['copies'];
		c_board = decklist[c]['board'];

		var sets = players_picks[active_player];
		var insets = card_index[c_name]['sets'];

		var color = "black";

		for(var s = 0; s < insets.length; s++) {
			if(sets.includes(insets[s]) == true) {
				color = "green"
				break;
			}
		}

		for(var una = 0; una <  predictions_array[index][1]['unavailable'].length; una++) {
			var una_name = predictions_array[index][1]['unavailable'][una]['name'];
			if(una_name == c_name) {
				color = "red";
				break;
			}
		}
		markup = markup + '<tr style=\"color:' + color + '\"><td id=\"' + encode(c_name) + '\">' + c_copies + 'x '+ c_name + "</td><td>" + c_board + "</td></tr>";
	}

	$('#player-details').append(markup);




	//console.log(predictions_array[index][1]['unavailable']);


}









