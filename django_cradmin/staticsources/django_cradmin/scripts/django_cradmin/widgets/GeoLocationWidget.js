import AbstractWidget from "ievv_jsbase/widget/AbstractWidget";


export default class GeoLocationWidget extends AbstractWidget {
  constructor(element, widgetInstanceId) {
    super(element, widgetInstanceId);
    this.locationSuccess = this.locationSuccess.bind(this);
    this.locationError = this.locationError.bind(this);
    if (this.config.signalNameSpace == null) {
      throw Error("signalNameSpace is required!");
    }
    this.getLocation();
  }

  getDefaultConfig() {
    return {
      enableHighAccuracy: true,
      watchLocation: true,
      signalNameSpace: null,
    }
  }

  locationSuccess(position){
    new window.ievv_jsbase_core.SignalHandlerSingleton().send(
      `${this.config.signalNameSpace}.GeoLocationUpdate`,
      position);
  }

  locationError(error) {
    if (error.code == PositionError.code.PERMISSION_DENIED){
      new window.ievv_jsbase_core.SignalHandlerSingleton().send(
      `${this.config.signalNameSpace}.GeoLocationPermissionDenied`,
      position);
    }
  }

  getLocation() {
    const options = {
      enableHighAccuracy: this.config.enableHighAccuracy
    };
    if (this.config.watchLocation) {
      this.watchPositionId = navigator.geolocation.watchPosition(this.locationSuccess, this.locationError, options);
    } else {
      navigator.geolocation.getCurrentPosition(this.locationSuccess, this.locationError, options);
    }
  }

  destroy() {
    if (this.watchPositionId != undefined) {
      navigator.geolocation.clearWatch(this.watchPositionId);
    }
  }
}
