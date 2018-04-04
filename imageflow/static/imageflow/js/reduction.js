function setupRunReductions() {
  $('.js-run-reductions').on('click', function() {
    $.post('/analysis/' + window.analysisId + '/set_reduction_status', {
      status: 'PENDING'
    }, function(data) {
      $('.page-loader').show();
      pollReductionStatus();
    });
    return false;
  });
}

function pollReductionStatus() {
  $.get('/analysis/' + window.analysisId + '/get_reduction_status', function(data) {
    if (data.status === 'COMPLETE') {
      $('.page-loader').hide();
      alert('Your reduction has completed. Press OK to refresh.');
      window.location.reload();
    } else {
      setTimeout(pollReductionStatus, 1000);
    }
  });
}

function setupAddToLightcurve() {
  var hasBeenAdded = false;
  $('.js-add-to-lightcurve').on('click', function() {
    if (hasBeenAdded) {
      return false;
    }
    var $btn = $(this);
    $.post('/lightcurve/' + window.lightcurveId + '/add_image_toggle', {
      'analysisId' : window.analysisId,
    }, function(data) {
      if (data.success) {
        hasBeenAdded = true;
        $btn.text('View light curve').on('click', function() {
          window.location.href = '/lightcurve/' + window.lightcurveId + '/plot';
          return false;
        });
      } else {
        alert('Something went wrong. Changes were not applied to this image.');
      }
    });
    return false;
  });
}

$(function() {
  setupListener('set_color_index_1',
                $('#select-color-index-1'),
                $('#select-color-index-success'),
                $('#select-comparison-image-failure'));

  setupListener('set_color_index_2',
                $('#select-color-index-2'),
                $('#select-color-index-success'),
                $('#select-comparison-image-failure'));

  setupListener('set_second_order_extinction',
                $('#second-order-extinction'),
                $('#second-order-extinction-success'),
                $('#second-order-extinction-failure'));

  setupListener('set_color_index_manual',
                $('#color-index-manual'),
                $('#color-index-manual-success'),
                $('#color-index-manual-failure'));

  setupRunReductions();
  setupAddToLightcurve();

  setupMagnitudeChecks($('.plot-container'),
                       'standard',
                       window.reducedStars,
                       window.reducedStars,
                       true /* comparisonStarsOnly*/ );
});
