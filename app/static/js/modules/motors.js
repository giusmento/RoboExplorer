// DISABLE MOTOR:
// motor_num: 0 to 3
function disable_motor(motor_num){
    console.log("disable motor: " + motor_num)
    $("#switch-motor-" + motor_num).bootstrapToggle('off')
}

// ENABLE MOTOR:
// motor_num: 0 to 3
function enable_motor(motor_num){
    console.log("enable motor: " + motor_num)
    $("#switch-motor-" + motor_num).bootstrapToggle('on')
}

// ENABLE SPEED
function enable_motor_speed(motor_num){
    console.log("enable motor speed " + motor_num)
    $( "#slider-motor-" + motor_num ).slider( "option", "disabled", false );
}

// ENABLE SPEED
function disable_motor_speed(motor_num){
    console.log("disable motor speed " + motor_num)
    $( "#slider-motor-" + motor_num ).slider( "option", "disabled", true );
}

// TOGGLE MOTOR SPEED
function toggle_motor_speed(motor_num){
    console.log("toggle motor speed " + motor_num)
    var disabled = $( "#slider-motor-" + motor_num ).slider( "option", "disabled" );
    console.log("toggle - disabled::" + disabled)
    $( "#slider-motor-" + motor_num ).slider( "option", "disabled", ! disabled );
    var enable_motor = document.getElementById("switch-motor-" + motor_num).checked
    console.log("enable_motor::" + enable_motor)
    set_motor_enabled_api(motor_num, enable_motor)
}

// SET MOTOR SPEED
function set_motor_speed(motor_num, speed){
    console.log("set motor " + motor_num + " speed " + speed)
    $( "#slider-motor-" + motor_num ).slider("option", "value", speed);
    $( "#slider-label-motor-" + motor_num ).text( String(speed))
}

function set_motor_speed_api(motor_num, speed){
    $.ajax({
            type: 'POST',
            url: 'http://localhost:5000/motors/' + motor_num,
            data: JSON.stringify({speed: speed}),
            contentType: 'application/json',
            success: function(result){
                console.log(result)
            },
            error: function(error){
                $("#motor-" + motor_num + "-error").text("error on setting speed")
            }
    });
}

function set_motor_enabled_api(motor_num, enabled){
    $.ajax({
            type: 'POST',
            url: 'http://localhost:5000/motors/' + motor_num,
            data: JSON.stringify({enabled: enabled}),
            contentType: 'application/json',
            success: function(result){
                console.log(result)
            },
            error: function(error){
                $("#motor-" + motor_num + "-error").text("error on setting speed")
            }
    });
}

function initialize_motors(){
    $(function() {

        // MOTOR 1 :SLIDER
        var handle_motor0 = $( "#slider-label-motor-0" );
        $( "#slider-motor-0" ).slider({
          min: 0,
          max: 10,
          value: 0,
          disabled: false,
          create: function() {
            handle_motor0.text( $( this ).slider( "value" ) );
          },
          slide: function( event, ui ) {
            handle_motor0.text( ui.value );
            console.log("change speed to:" + ui.value)
            set_motor_speed_api(0, ui.value)
          }
        });

        // MOTOR 2 :SLIDER
        var handle_motor1 = $( "#slider-label-motor-1" );
        $( "#slider-motor-1" ).slider({
          min: 0,
          max: 10,
          value: 0,
          disabled: true,
          create: function() {
            handle_motor1.text( $( this ).slider( "value" ) );
          },
          slide: function( event, ui ) {
            handle_motor1.text( ui.value );
            set_motor_speed_api(1, ui.value)
          }
        });

        // MOTOR 3 :SLIDER
        var handle_motor2 = $( "#slider-label-motor-2" );
        $( "#slider-motor-2" ).slider({
          min:0,
          max: 10,
          value: 0,
          disabled: true,
          create: function() {
            handle_motor2.text( $( this ).slider( "value" ) );
          },
          slide: function( event, ui ) {
            handle_motor2.text( ui.value );
            set_motor_speed_api(2, ui.value)
          }
        });

        // MOTOR 4 :SLIDER
        var handle_motor3 = $( "#slider-label-motor-3" );
        $( "#slider-motor-3" ).slider({
          min: 0,
          max: 10,
          value: 0,
          disabled: true,
          create: function() {
            handle_motor3.text( $( this ).slider( "value" ) );
          },
          slide: function( event, ui ) {
            handle_motor3.text( ui.value );
            set_motor_speed_api(3, ui.value)
          }
        });
        });
}