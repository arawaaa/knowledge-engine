import React from 'react';

type globalState = {
  loggedIn: boolean;
  setLoggedIn: React.Dispatch<React.SetStateAction<boolean>>;
  token: number | undefined;
  setToken: React.Dispatch<React.SetStateAction<number | undefined>>;
} | undefined

export const GlobalCtx = React.createContext<globalState>(undefined)
