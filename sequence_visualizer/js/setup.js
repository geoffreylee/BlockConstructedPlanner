var me = "Geoff";
var mypicks = [];
var unavailable = [];
var assembled = [];

var tempchosen = [];
//var tempassembled =[];
var deck_size = 0
var total_assembled = 0;

function encode(name){ 
	name = name.replace(/\(/g, '_leftparens_');
	name = name.replace(/\)/g, '_rightparens_');
	name = name.replace(/:/g, '_colon_');
	name = name.replace(/'/g, '_apostrophe_');
	return name.replace(/ /g,'_spacehere_'); 
}

function unencode(sid){ 
	sid = sid.replace(/_leftparens_/g, '(');
	sid = sid.replace(/_rightparens_/g, ')');
	sid = sid.replace(/_colon_/g, ':');
	sid = sid.replace(/_apostrophe_/g, '\'');
	return sid.replace(/_spacehere_/g, ' '); 
}

function recalculate_assembled(acquired_sets){
	for(var set in deck_sequence) {
		var name = deck_sequence[set][0]
		if(acquired_sets.includes(name)){
			for(card in deck_sequence[set][1]['relevant_cards']) {
				var cardname = deck_sequence[set][1]['relevant_cards'][card][0]
				console.log(cardname)
				if(cardname in assembled == false) {
					assembled[cardname] = decklist[cardname];
				}
			}
		}
	}
}

function redraw(){
	$('#sequence tbody').empty()
	$('#assembled tbody').empty()	
	recalculate_assembled(mypicks.concat(tempchosen));
	draw_assembled_list(assembled)
	reasses_priorities(assembled, mypicks.concat(tempchosen));
	reasses_priorities(assembled, mypicks.concat(tempchosen)); // extremely jank but the second call fixes index issues
	redraw_sequence();
}


function init_already_assembled(){
	//basics
	for(var n in decklist){
		if(n == "Mountain" || n == "Forest" || n == "Plains" || n == "Swamp" || n == "Island"){
			if(n in assembled == false){
				assembled[n] = decklist[n];
			}
		}
	}
	for(var set in deck_sequence){
		var name = deck_sequence[set][0];
		if(mypicks.includes(name)) {
			for(card in deck_sequence[set][1]['relevant_cards']){
				name = deck_sequence[set][1]['relevant_cards'][card][0];
				if(name in assembled == false){
					assembled[name] = decklist[name];
				}  
			}
		}
	}
}

function redraw_sequence(){
	for(var set in deck_sequence){
		var relevant_tooltip = [];
		var name = deck_sequence[set][0];

		for(card in deck_sequence[set][1]['relevant_cards']){
			var relevant_name = deck_sequence[set][1]['relevant_cards'][card][0];
			relevant_tooltip.push(relevant_name);
		}
		if(unavailable.includes(name)){
			availability = 'unavailable';
		}
		else{
			availability = 'available';
		}
	
		var markup = '<tr id=\"' + encode(name) + '\" class=\"'+availability+' set\" title=\"' + relevant_tooltip.join(", ") + '\"><td>' + name + '</td></tr>';
		$('#sequence').append(markup);
	}
}

function recalculate_sequence(deck_seq){
	deck_seq.sort(function(a,b){
		a_score = 0.0;
		b_score = 0.0;
		
		for(var card in a[1]['relevant_cards'])
		{
			freq = a[1]['relevant_cards'][card]
			copies = decklist[card]
			a_score += copies/freq
		}

		for(var card in b[1]['relevant_cards'])
		{
			freq = b[1]['relevant_cards'][card]
			copies = decklist[card]
			b_score += copies/freq
		}
		return (b_score * b[1]['max_clump_score']) - (a_score * a[1]['mac_clump_score']); // Reverse Order
	});
}

function draw_already_picked(){

	for(var pick in picks_table[me]){
		var set = picks_table[me][pick][0];
		mypicks.push(set);
		var markup = '<tr id=\"' + encode(set) + '\" class=\"set\"><td>' + set + '<td></tr>';
		$('#chosen').append(markup);
	}
}

function recalculate_unavailability_restrictions(){
	for(set in deck_sequence){
		var name = deck_sequence[set][0]
	}
	if(unavailable.includes(name)) {
		for(var card in deck_sequence[set][1]['relevant_cards']){
			cardname = deck_sequence[set][1]['relevant_cards'][card][0];
			for(var otherset in deck_sequence) {
				if(otherset == set) {
					continue;
				}
				for(var overlap in deck_sequence[otherset]['relevant_cards'])
				{
					if(deck_sequence[otherset]['relevant_cards'][overlap][0] == cardname){
						// lower redundancy for each set taken
						deck_sequence[otherset]['relevant_cards'][overlap][1] -= 1;
					}
				}
			}
		}
	}
}

function populate_unavailable(){
	for(person in picks_table){
		if(person == me){
			continue
		} 
		for(pick in picks_table[person]){
			set = picks_table[person][pick][0];
			unavailable.push(set);
		}
	}
}
function draw_assembled_list(assembled){
	total_assembled = 0
	$('#Forest').addClass('basic');
	$('#Plains').addClass('basic');
	$('#Mountain').addClass('basic');
	$('#Swamp').addClass('basic');
	$('#Island').addClass('basic');
	for(var card in assembled){
		var copies = decklist[card];
		total_assembled += copies;
		var markup = '<tr><td>' + copies + ' ' + card + '</td></tr>';
		$('#assembled').append(markup);
		$('#'+encode(card)).addClass('owned');
	}

	var markup = '<tr><td id=progress>' + total_assembled + ' of ' + deck_size + '</td></tr>';
	$('#assembled').append(markup);
}



	

function reasses_priorities(assembled, acquired_sets){
	for(var set = deck_sequence.length - 1; set >=0; set--){
	
		var name = deck_sequence[set][0];
		//console.log(name)
		if(acquired_sets.includes(name)){
			//console.log("we have")
			deck_sequence.splice(set, 1);
			continue;
		}
		
		for(card in deck_sequence[set][1]['relevant_cards']){
			relevant_name = deck_sequence[set][1]['relevant_cards'][card][0];
			//console.log(deck_sequence[set][1]['relevant_cards'][card][0])
			if(relevant_name in assembled){
				deck_sequence[set][1]['relevant_cards'].splice(card,1)
			}
		}
		if(deck_sequence[set][1]['relevant_cards'].length==0){
			//console.log(name + " spliced to 0")
			deck_sequence.splice(set, 1);
		} 	
	}
	recalculate_sequence(deck_sequence);
}

function draw_decklist() {
	for(var card in decklist){
		copies = decklist[card];
		var markup = '<tr id=\"' +encode(card) + '\"><td>' + copies + ' '+ card + '</td></tr>';
		$('#decklist').append(markup);
		deck_size += copies;
	}
	var markup = '<tr id="total_deck_size"><td>' + deck_size +  ' of ' + deck_size + ' cards</td></tr>';
	$('#decklist').append(markup)
}


populate_unavailable();
recalculate_unavailability_restrictions()
draw_decklist();

// init
draw_already_picked()
init_already_assembled()
draw_assembled_list(assembled)

reasses_priorities(assembled, mypicks);
reasses_priorities(assembled, mypicks); // extremely jank but the second call fixes index issues
redraw_sequence();
