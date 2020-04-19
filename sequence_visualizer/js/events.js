$(document).ready(function(){
	$('#playername').text(me + "'s Player Perspective")
	//$('#sequence').tooltip();
	$('#sequence').on('click', '.available', function(){
		console.log("click")
		var id = $(this).attr('id');
		var markup = '<tr id=\"' + id + '\" class=\"temp_chosen\"><td>' + unencode(id) + '</td></tr>';
		$('#chosen').append(markup);
		$(this).remove();
		tempchosen.push(unencode(id));
		redraw();
	});
});