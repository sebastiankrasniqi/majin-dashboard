import type { Config, Context } from '@netlify/edge-functions'

const SCANNER_UA = /(sqlmap|nikto|acunetix|nessus|nmap|masscan|zgrab|dirbuster|gobuster|wpscan|fuzz|havij|morfeus|netsparker|openvas|pangolin|qualys|skipfish|w3af|whatweb|wfuzz|hydra)/i

const EXPLOIT_PATH = /(^|\/)(wp-admin|wp-login|wp-content|wp-includes|xmlrpc\.php|phpmyadmin|pma|myadmin|adminer|\.env|\.git|\.svn|\.hg|\.aws|\.ssh|\.well-known\/acme-challenge\/\.\.|cgi-bin|actuator|server-status|server-info|boaform|HNAP1|hudson|jenkins|config\.json|credentials|id_rsa|\.docker)(\/|$)/i

const EXPLOIT_EXT = /\.(php|phtml|asp|aspx|jsp|cgi|bak|old|swp|sql|env|log)$/i

const TRAVERSAL = /(\.\.[\/\\])|(%2e%2e(%2f|%5c))/i

const ALLOWED_METHODS = new Set(['GET', 'HEAD', 'OPTIONS'])

export default async (req: Request, _context: Context): Promise<Response | void> => {
  try {
    const method = req.method.toUpperCase()

    if (!ALLOWED_METHODS.has(method)) {
      return new Response('Method Not Allowed', {
        status: 405,
        headers: { Allow: 'GET, HEAD, OPTIONS' },
      })
    }

    const ua = req.headers.get('user-agent') ?? ''
    if (SCANNER_UA.test(ua)) {
      return new Response('Forbidden', { status: 403 })
    }

    let url: URL
    try {
      url = new URL(req.url)
    } catch {
      return
    }

    if (TRAVERSAL.test(url.pathname) || TRAVERSAL.test(url.search)) {
      return new Response('Not Found', { status: 404 })
    }

    if (EXPLOIT_PATH.test(url.pathname) || EXPLOIT_EXT.test(url.pathname)) {
      return new Response('Not Found', { status: 404 })
    }

    if (url.pathname.length > 1024 || url.search.length > 2048) {
      return new Response('Request-URI Too Long', { status: 414 })
    }
  } catch (err) {
    console.error('shield edge function error:', err)
    return
  }
}

export const config: Config = {
  path: '/*',
  excludedPath: [
    '/style.css',
    '/*.css',
    '/*.js',
    '/*.png',
    '/*.jpg',
    '/*.jpeg',
    '/*.gif',
    '/*.svg',
    '/*.webp',
    '/*.ico',
    '/*.woff',
    '/*.woff2',
  ],
}
