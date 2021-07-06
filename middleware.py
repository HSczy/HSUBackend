class CORSComponent:
    def process_response(self, req, resp, resource, req_succeeded):
        resp.set_header('Access-Control-Allow-Origin', '*')
        # resp.set_header('Access - Control - Expose - Headers','Authorization')

        if (req_succeeded
                and req.method == 'OPTIONS'
                and req.headers.get('ACCESS-CONTROL-REQUEST-METHOD')
        ):
            allow = req.get_param('Allow')
            resp.delete_header('Allow')

            allow_headers = req.get_param(
                'Access-Control-Request-Headers',
                default='*'
            )

            resp.set_headers((
                ('Access-Control-Allow-Methods', allow),
                ('Access-Control-Allow-Headers', allow_headers),
                ('Access-Control-Max-Age', '86400')
            ))