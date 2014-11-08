
angular.module('Dashboard')
.controller('NotesController', ['$scope','Note', NotesController]);

function NotesController($scope,$Note) {
	var noteHash={}, noteDefaults={};
	$scope.getResponses = function(note){
		if(note)
			return noteHash[note.id];
		else
			return noteHash[null];
	};
	
//	$scope.notes = $Note.query();
	$scope.setNoteDefaults = function(defaults){
		noteDefaults = defaults;
		
	};
	$scope.save = function(note){
		if(note.id)
			note.$save();
		else
			note.$create();
	};
	$scope.newNote = function(){
		var note = new $Note(noteDefaults);
		note.editing=true;
		note.parent = null;
		$scope.addNote(note);
	};
	$scope.deleteNote = function(note){
		if (!confirm("Are you sure you want to delete this note and all responses?"))
			return;
		var parent = note.parent;
		var id = note.id;
		var removeFunc = function() {
			for (var i in noteHash[parent]){
				if (noteHash[parent][i].id == id)
					noteHash[parent].splice(i,1);
			}
		};
		if(!id){
			removeFunc();
			return;
		}
		note.$remove(removeFunc);
	};
	$scope.respond = function(parent){
		var note = new $Note(noteDefaults);
		note.parent=parent.id;
		note.editing=true;
		$scope.addNote(note);
	};
	$scope.addNote = function(note){
		console.log(note);
		if(!noteHash[note.parent])
			noteHash[note.parent] = [];
		noteHash[note.parent].push(note);
	};
	$scope.init = function(){
		$scope.notes = $Note.query(noteDefaults,function() {
			angular.forEach($scope.notes,function(note){
				$scope.addNote(note);
			});

			console.log(noteHash);
		});
	}
	
	
}

