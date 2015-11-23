BASE_URL = "http://192.168.0.25:8000"
POSITION_LIST_ENDPOINT = BASE_URL + '/api/position'
POSITION_DETAIL_ENDPOINT = POSITION_LIST_ENDPOINT + '/{0}'
MOVE_UP_ENDPOINT = BASE_URL + '/api/desk/up'
MOVE_DOWN_ENDPOINT = BASE_URL + '/api/desk/down'
STOP_ENDPOINT = BASE_URL + '/api/desk/stop'


function get_positions() {
  $.ajax({
      url: POSITION_LIST_ENDPOINT,
      type: "GET",
      contentType: "application/json",
      dataType: "json",
  }).then(function(data) {
     console.log(data)
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
  $.ajax({
      url: POSITION_LIST_ENDPOINT,
      type: "POST",
      data : JSON.stringify(position_data),
      contentType: "application/json",
      dataType: "json",
  }).then(function(data) {
     console.log(data);
     return data;
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
