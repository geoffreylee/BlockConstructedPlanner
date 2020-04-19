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
