export class ParseMessage {
  constructor(json_string) {
    this.sender = null;
    this.type = null;
    this.payload = null;
    this.timestamp = null;
    this.parse(json_string);
  }

  parse(json_string) {
    var object = JSON.parse(json_string);
    this.sender = object._Message__sender;
    this.type = object._Message__type;
    this.payload = object._Message__payload;
    this.timestamp = object._Message__timestamp;
  }
}
