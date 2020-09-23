export class WsMessage{
    #type="";
    #sender="";
    #destination="";
    #payload="";
    #timestamp="";

    constructor(type, sender, destination, payload){
        this.#type = type
        this.#sender = sender
        this.#destination = destination
        this.#payload = payload
        this.#timestamp = Date.now();
    }

    getType(){
        return this.#type
    }
    getSender(){
        return this.#sender
    }
    getDestination(){
        return this.#destination
    }
    getPayload(){
        return this.#payload
    }
    getTimestamp(){
        return this.#timestamp
    }
    stringify(){
        return JSON.stringify({ 
            type: this.#type, 
            sender: this.#sender, 
            destination: this.#destination,
            timestamp: this.#timestamp,
            payload: this.#payload 
        })
    }
}