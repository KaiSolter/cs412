import { createContext, ReactNode, useContext, useMemo, useState } from 'react';

type AuthContextValue = {
  token: string | null;
  profileId: number | null;
  setToken: (token: string | null) => void;
  setProfileId: (profileId: number | null) => void;
  setAuth: (token: string | null, profileId: number | null) => void;
  logout: () => void;
};

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

type AuthProviderProps = {
  children: ReactNode;
};

export function AuthProvider({ children }: AuthProviderProps) {
  const [token, setToken] = useState<string | null>(null);
  const [profileId, setProfileId] = useState<number | null>(null);

  const value = useMemo(
    () => ({
      token,
      profileId,
      setToken,
      setProfileId,
      setAuth: (nextToken: string | null, nextProfileId: number | null) => {
        setToken(nextToken);
        setProfileId(nextProfileId);
      },
      logout: () => {
        setToken(null);
        setProfileId(null);
      },
    }),
    [token, profileId]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }

  return context;
}
