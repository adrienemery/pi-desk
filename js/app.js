BASE_URL = "http://192.168.0.25:8000"
// BASE_URL = "http://localhost:8000"
POSITION_LIST_ENDPOINT = BASE_URL + '/api/position'
POSITION_DETAIL_ENDPOINT = POSITION_LIST_ENDPOINT + '/{0}'
MOVE_UP_ENDPOINT = BASE_URL + '/api/desk/up'
MOVE_DOWN_ENDPOINT = BASE_URL + '/api/desk/down'
MOVE_TO_POSITION_ENDPOINT = BASE_URL + '/api/desk/position/{0}'
STOP_ENDPOINT = BASE_URL + '/api/desk/stop'
DESK_ENDPOINT = BASE_URL + '/api/desk'

var height = null
var positions = [];

function update_position_list() {
  var to_append = ''
  $.each(positions, function(index, position){
    to_append += '<li class="list-group-item">' + position.name;
    to_append += '<button type="button" class="btn btn-default btn-sm" onclick="delete_position(' + String(position.id) +  ')"> <span class="glyphicon glyphicon-minus" aria-hidden="true"></span></button>';
    to_append += '<button type="button" class="btn btn-default btn-sm"> <span class="glyphicon glyphicon-pencil" aria-hidden="true"></span></button>';
    to_append += '<button class="btn btn-sm btn-success" type="button" name="on_btn" onclick="move_to_position(' + String(position.id) + ')">Go</button>';
    to_append += '</div>  </li>';
  });
  $("#posiiton-list").html(to_append);
}

function get_positions() {
  $.ajax({
      url: POSITION_LIST_ENDPOINT,
      type: "GET",
      contentType: "application/json",
      dataType: "json",
  }).then(function(data) {
     console.log(data);
     positions = data.objects;
     update_position_list();
     get_height();
  });
}

function get_height() {
  $.ajax({
      url: DESK_ENDPOINT,
      type: "GET",
      contentType: "application/json",
      dataType: "json",
  }).then(function(data) {
     console.log(data);
     height = data.height
  });
}

$("#down_btn")
  .mouseup(function() {
    stop_desk();
  })
  .mousedown(function() {
    move_down();
});

$("#up_btn")
  .mouseup(function() {
    stop_desk();
  })
  .mousedown(function() {
    move_up();
});


// Load positions on first load
$(document).ready(function() {
  get_positions();
});


function move_up() {
  $.ajax({
      url: MOVE_UP_ENDPOINT,
      type: "POST",
      contentType: "application/json",
      dataType: "json",
  }).then(function(data) {
     console.log(data);
     get_height();
     return data;
  });
};


function move_down() {
  $.ajax({
      url: MOVE_DOWN_ENDPOINT,
      type: "POST",
      contentType: "application/json",
      dataType: "json",
  }).then(function(data) {
     console.log(data);
     get_height();
     return data;
  });
};

function move_to_position(position_id) {
  url = String.format(MOVE_TO_POSITION_ENDPOINT, position_id)
  $.ajax({
      url: url,
      type: "POST",
      contentType: "application/json",
      dataType: "json",
  }).then(function(data) {
     console.log(data);
     return data;
  });
};


function stop_desk() {
  $.ajax({
      url: STOP_ENDPOINT,
      type: "POST",
      contentType: "application/json",
      dataType: "json",
  }).then(function(data) {
     console.log(data);
     get_height();
     return data;
  });
};


function add_position() {
  vex.dialog.open({
    message: 'Create a new setpoint',
    input: "<input name=\"name\" type=\"text\" placeholder=\"Name (required)\" required />\n \
            <input name=\"height\" type=\"number\" placeholder=\"Don't enter a value to use current height\" />",
    buttons: [
      $.extend({}, vex.dialog.buttons.YES, {
        text: 'Save'
      }), $.extend({}, vex.dialog.buttons.NO, {
        text: 'Back'
      })
    ],
    callback: function(data) {
      if (data === false) {
        return console.log('Cancelled');
      }
      new_position = create_position(data);
      return;
    }
  });
};


function create_position(position_data) {
  if (position_data.height == "") {
    position_data.height = height;
  }
  $.ajax({
      url: POSITION_LIST_ENDPOINT,
      type: "POST",
      data : JSON.stringify(position_data),
      contentType: "application/json",
      dataType: "json",
  }).then(function(data) {
     console.log(data);
     get_positions();
     return data;
  });
}


function delete_position(position_id) {
  url = String.format(POSITION_DETAIL_ENDPOINT, position_id)
  $.ajax({
      url: url,
      type: "DELETE",
      contentType: "application/json",
      dataType: "json",
  }).then(function(data) {
     get_positions();
  });
}


function update_position(position_data, id) {
  url = String.format(POSITION_DETAIL_ENDPOINT, id)
  $.ajax({
      url: url,
      type: "PATCH",
      data : JSON.stringify(position_data),
      contentType: "application/json",
      dataType: "json",
  }).then(function(data) {
     console.log(data);
     return data;
  });
}


String.format = function() {
  var s = arguments[0];
  for (var i = 0; i < arguments.length - 1; i++) {
    var reg = new RegExp("\\{" + i + "\\}", "gm");
    s = s.replace(reg, arguments[i + 1]);
  }

  return s;
}
