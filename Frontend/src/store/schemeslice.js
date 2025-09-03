// schemeSlice.js
import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  scheme: [],
};

const schemeSlice = createSlice({
  name: "scheme",
  initialState,
  reducers: {
    setScheme: (state, action) => {
      state.scheme = action.payload;
    },
  },
});

export const { setScheme } = schemeSlice.actions; // export action
export default schemeSlice.reducer; // fixed export
