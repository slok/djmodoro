$(document).ready(function() {

  var selectedObject = null; // This will be the object to update when finished
  var started = null;
  var shouldFinish = null;
  var finished = null;
  var firstTime = true;

  // Ask before leaving
  $(window).on('beforeunload', function(){
    return 'Are you sure you want to leave?';
  });

  // Prepare the form events
  create_run();
  update_run();

  function newClock(){

    started = moment.utc();
    shouldFinish = started.clone().add(25, 'minutes');

    // Create the progress bar
    $('#progress-bar').attr('aria-valuemin', started.unix())
    $('#progress-bar').attr('aria-valuemax', shouldFinish.unix())

    // Set the events for the counter
    if (firstTime){
        $("#clock").countdown(shouldFinish.toDate(), function(event) {
          $(this).text(
            event.strftime('%M:%S')
          );}).on('update.countdown', function(event) {
              // Update the progress bar
              $('#progress-bar').attr('aria-valuenow', moment.utc().unix());

              var totalSecondsToFinish = shouldFinish.unix() - started.unix();
              var secondsNow = totalSecondsToFinish - (shouldFinish.unix() - moment.utc().unix());
              var barValue = "width: "  + secondsNow * 100 / totalSecondsToFinish + "%";
              $('#progress-bar').attr('style', barValue);
          }).on('finish.countdown', function(event) {
              finished = moment.utc();

              // Update the object
              $("#task-form-update").submit();

              // Show the alert
              alert("Time to rest!")

              // Enable for another run
              $("#start-counter").prop('disabled', false);
              $("#start-counter").text('Start!');
          });
        firstTime = false;
    } else{
      $('#clock').countdown(shouldFinish.toDate());
    }
  }

  //Button click handler
  $( "#start-counter" ).click(function() {
    // Start counter
    newClock()
    $("#clock").countdown('start');

    // Disable button
    $("#start-counter").prop('disabled', true);
    $("#start-counter").text('work!');

    $("#task-form").submit();

  });

  // functions
  function create_run(){
    $("#task-form").submit(function(event) {
      // Add new values to the form
      $("#task-form").find(
        'input[name="start"]').val(started.format("YYYY-M-DD HH:mm:ss"))
      // Ajax request
      $.ajax({
        type: $("#task-form").attr('method'),
        url: $("#task-form").attr('action'),
        data: $("#task-form").serialize(), // serializes the form's elements.
        success: function(data){
          selectedObject = data['pk'];
        },
        fail: function(data){
          alert("Something failed!");
        }
      });

      event.preventDefault(); //STOP default action
      return false; // avoid to execute the actual submit of the form.
    });
  }

  function update_run(){
   // Send ajax request
    $("#task-form-update").submit(function(event) {

      // Add new values to the form
      $('#task-form-update').find(
        'input[name="task"]').val($( "#id_task" ).val())

      $('#task-form-update').find(
        'input[name="start"]').val(started.format("YYYY-M-DD HH:mm:ss"))

      $('#task-form-update').find(
        'input[name="finish"]').val(finished.format("YYYY-M-DD HH:mm:ss"))

      // Ajax request
      $.ajax({
        type: $("#task-form-update").attr('method'),
        url: $("#task-form-update").attr('action') + "/" + selectedObject,
        data: $("#task-form-update").serialize(), // serializes the form's elements.
        fail: function(data){
          alert("Something failed!");
        }
      });

      event.preventDefault(); //STOP default action
      return false; // avoid to execute the actual submit of the form.
    });
  }
});