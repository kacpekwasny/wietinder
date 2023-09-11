import { reactive } from "vue";
import { io } from "socket.io-client";

import {getBackendHostname} from "../common/requests";

export const state = reactive({
  connected: false,
  fooEvents: [],
  barEvents: []
});

export const socket = io(getBackendHostname());


socket.on("connect", () => {
  state.connected = true;
  console.log('connect')
});

socket.on("disconnect", () => {
  state.connected = false;
  console.log('disconnect')
});

socket.on("foo", (...args) => {
  state.fooEvents.push(args);
  console.log('foo')
});

socket.on("bar", (...args) => {
  state.barEvents.push(args);
  console.log('bar')
});

