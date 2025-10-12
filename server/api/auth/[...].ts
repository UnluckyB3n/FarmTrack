import Google from '@auth/core/providers/google';
import { NuxtAuthHandler } from '#auth';

export default NuxtAuthHandler({
  providers: [
    // Call useRuntimeConfig inside the handler to avoid circular import issues
     // @ts-expect-error Google provider type mismatch is safe to ignore
    Google({
      clientId: useRuntimeConfig().GOOGLE_CLIENT_ID || '',
      clientSecret: useRuntimeConfig().GOOGLE_CLIENT_SECRET || '',
    })
  ]
});
