export class FixedLengthArray {
  constructor(length) {
    this.arr = [];
    this.length = length;
  }

  push(item) {
    this.arr.push(item);
    if (this.arr.length > this.length) {
      this.arr.shift();
    }
  }
}
