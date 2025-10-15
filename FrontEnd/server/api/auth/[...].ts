import { NuxtAuthHandler } from '#auth';
import GoogleProvider from 'next-auth/providers/google';

// Use this to access your environment variables defined in nuxt.config.ts -> runtimeConfig.private
const runtimeConfig = useRuntimeConfig();

export default NuxtAuthHandler({
  // The secret is needed to sign the JWT/session token.
  secret: runtimeConfig.private.NEXTAUTH_SECRET,

  // A list of authentication providers
  providers: [
    // --- Google Provider Configuration ---
    GoogleProvider.default({
      // Fetch the Client ID from the private runtime config
      clientId: runtimeConfig.private.GOOGLE_CLIENT_ID,
      
      // Fetch the Client Secret from the private runtime config
      clientSecret: runtimeConfig.private.GOOGLE_CLIENT_SECRET,
      
      // Note: Scopes define what user data you request. 
      // 'openid' and 'profile' are required for basic sign-in.
      authorization: {
        params: {
          scope: 'openid profile email',
        },
      },
    }),
    // You would add other providers (GitHub, etc.) here if needed
  ],
  
  // Custom pages, optional but good for professional apps
  pages: {
    // This tells Auth.js to redirect to your custom sign-in page,
    // otherwise it uses a built-in one.
    // If you don't have a custom page yet, you can comment this out.
    signIn: '/login', 
  },
  
  // Optional: Add callbacks if you need to modify the session or JWT
  // callbacks: {
  //   session: ({ session, token }) => {
  //     // Attach userId or other custom data to the session
  //     // session.user.id = token.sub; 
  //     return session;
  //   },
  // },
});
