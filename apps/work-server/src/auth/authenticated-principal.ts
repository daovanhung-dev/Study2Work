/** Claims that are safe for Work domain authorization to consume directly. */
export interface AuthenticatedPrincipal {
  subject: string;
  sessionId: string;
  tokenId: string;
  authVersion: number;
  scopes: string[];
}
