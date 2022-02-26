(function (win, $) {
    if (typeof (win.inma) === 'undefined') {
        win.inma = {};
    }

    var inma = win.inma;
    inma.requests = inma.requests || {};

    inma.requests.getUrlWithContextPath = function (URL) {
        return URL;
    };

    inma.requests.changePage = function (page) {
        window.location.href = inma.requests.getUrlWithContextPath(page);
    };

    inma.requests.getCurrentUrl = function () {
        var url = window.location.pathname;
        return url.includes('?') ? url.substring(0, url.indexOf('?')) : url;
    }

    inma.requests.refreshPage = function () {
        window.location.reload();
    }

    inma.requests.getCsrfToken = function () {
        return $('[name="csrfmiddlewaretoken"]').val();
    }

    inma.requests.getUrlParameter = function getUrlParameter(sParam) {
        var sPageURL = window.location.search.substring(1),
            sURLVariables = sPageURL.split('&'),
            sParameterName,
            i;

        for (i = 0; i < sURLVariables.length; i++) {
            sParameterName = sURLVariables[i].split('=');

            if (sParameterName[0] === sParam) {
                var newVar = sParameterName[1] === undefined ? true : decodeURIComponent(sParameterName[1]);
                return newVar;
            }
        }
    };


    function popupError(error) {
        var modalText = error.responseText;
        if (error.responseJSON) {
            modalText = '';
            $.each(error.responseJSON, function (k, v) {
                modalText += ('<p>' + k + ' : ');
                if ($.isArray(v)) {
                    $.each(v, function (index, value) {
                        if (index !== 0) {
                            modalText += ',<br>';
                        }
                        modalText += value;
                    });
                } else {
                    modalText += v;
                }
                modalText += '</p>\n';
            });
        }
    }

    inma.requests.get = function (path, params, option) {
        var $deferred = $.Deferred();
        option = option || {};
        var $url = inma.requests.getUrlWithContextPath(path);
        $.get($url, params).done(function (res) {
            $deferred.resolve(res);
        }).fail(function (data, status, error) {
            var error = {
                fail: true,
                url: $url,
                method: 'GET',
                params: params,
                status: data.status,
                errorCode: data.status,
                detailErrorCode: 0,
                message: data.statusText,
                detailMessage: undefined,
                stackTrace: undefined,
                statusText: data.statusText,
                responseText: data.responseText,
                responseJSON: data.responseJSON
            };
            if (!option.hidepopup) {
                popupError(error)
            }
            $deferred.reject(error);
        });
        return $deferred.promise();
    };

    inma.requests.post = function (path, params, option) {
        var $deferred = $.Deferred();
        option = option || {};
        var $url = inma.requests.getUrlWithContextPath(path);
        if (params) {
            params = JSON.stringify(params);
        }

        $.ajax({
            url: $url,
            method: 'post',
            type: 'json',
            contentType: 'application/json',
            data: params
        }).done(function (res) {
            $deferred.resolve(res);
        }).fail(function (data, status, error) {

            var error = {
                fail: true,
                url: $url,
                method: 'POST',
                params: params,
                status: data.status,
                errorCode: data.status,
                detailErrorCode: 0,
                message: data.statusText,
                detailMessage: undefined,
                stackTrace: undefined,
                statusText: data.statusText,
                responseText: data.responseText,
                responseJSON: data.responseJSON
            };
            if (!option.hidepopup) {
                popupError(error)
            }
            $deferred.reject(error);
        });
        return $deferred.promise();
    };

    inma.requests.upload = function (path, formData, option) {
        var $deferred = $.Deferred();
        option = option || {};
        var $url = inma.requests.getUrlWithContextPath(path);

        $.ajax({
            url: $url,
            type: 'POST',
            processData: false,
            contentType: false,
            data: formData,
        }).done(function (res) {
            $deferred.resolve(res);
        }).fail(function (data, status, error) {
            var error = {
                fail: true,
                url: $url,
                method: 'POST',
                params: params,
                status: data.status,
                errorCode: data.status,
                detailErrorCode: 0,
                message: data.statusText,
                detailMessage: undefined,
                stackTrace: undefined,
                statusText: data.statusText,
                responseText: data.responseText,
                responseJSON: data.responseJSON
            };
            if (!option.hidepopup) {
                popupError(error)
            }
            $deferred.reject(error);
        });
        return $deferred.promise();
    };


    inma.requests.create = inma.requests.post;

    inma.requests.put = function (path, params, option) {
        var $deferred = $.Deferred();
        option = option || {};
        var $url = inma.requests.getUrlWithContextPath(path);
        $.ajax({
            url: $url,
            method: 'put',
            type: 'json',
            data: params
        }).done(function (res) {
            $deferred.resolve(res);
        }).fail(function (data, status, error) {
            var error = {
                fail: true,
                url: $url,
                method: 'PUT',
                params: params,
                status: data.status,
                errorCode: data.status,
                detailErrorCode: 0,
                message: data.statusText,
                detailMessage: undefined,
                stackTrace: undefined,
                statusText: data.statusText,
                responseText: data.responseText,
                responseJSON: data.responseJSON
            };
            if (!option.hidepopup) {
                popupError(error)
            }
            $deferred.reject(error);
        });
        return $deferred.promise();
    };

    inma.requests.update = inma.requests.put;


    inma.requests.patch = function (path, params, option) {
        var $deferred = $.Deferred();
        option = option || {};
        var $url = inma.requests.getUrlWithContextPath(path);
        $.ajax({
            url: $url,
            method: 'patch',
            type: 'json',
            data: params
        }).done(function (res) {
            $deferred.resolve(res);
        }).fail(function (data, status, error) {
            var error = {
                fail: true,
                url: $url,
                method: 'PATCH',
                params: params,
                status: data.status,
                errorCode: data.status,
                detailErrorCode: 0,
                message: data.statusText,
                detailMessage: undefined,
                stackTrace: undefined,
                statusText: data.statusText,
                responseText: data.responseText,
                responseJSON: data.responseJSON
            };
            if (!option.hidepopup) {
                popupError(error)
            }
            $deferred.reject(error);
        });
        return $deferred.promise();
    };


    inma.requests.destroy = function (path, params, option) {
        var $deferred = $.Deferred();
        option = option || {};
        var $url = inma.requests.getUrlWithContextPath(path);

        if (params) {
            if (Object.keys(params) !== undefined && Object.keys(params).length > 0) {
                $url += '?';
            }
            for (var i = 0; i < Object.keys(params).length; i++) {
                if (Object.keys(params)[i] === undefined) {
                    break;
                }
                var key = Object.keys(params)[i];
                $url += key + '=' + encodeURIComponent(params[key]);
                if (i < Object.keys(params).length - 1) {
                    $url += '&';
                }
            }
            params = {};
        }

        $.ajax({
            url: $url,
            method: 'delete',
            type: 'json',
        }).done(function (res) {
            $deferred.resolve(res);
        }).fail(function (data, status, error) {
            var error = {
                fail: true,
                url: $url,
                method: 'DELETE',
                params: params,
                status: data.status,
                errorCode: data.status,
                detailErrorCode: 0,
                message: data.statusText,
                detailMessage: undefined,
                stackTrace: undefined,
                statusText: data.statusText,
                responseText: data.responseText,
                responseJSON: data.responseJSON
            };
            if (!option.hidepopup) {
                popupError(error)
            }
            $deferred.reject(error);
        });
        return $deferred.promise();
    };


    inma.requests.successToast = function (title, message) {
        toastr.success(message, title, {
            timeOut: 1000,
            closeButton: true,
            positionClass: 'toast-bottom-right',
        })
    }

})(window, jQuery);