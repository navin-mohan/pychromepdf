import subprocess
import tempfile
import sys

class ChromePDF(object):

    # set headless chrome arguments
    _chrome_options = [
        '--headless',
        '--disable-gpu',
        '--no-margins',
    ]

    def __init__(self,chrome_exec,sandbox=True):
        '''
        Constructor
        chrome_exec (string) - path to chrome executable
        '''

        # check if the chrome executable path is non-empty string
        assert isinstance(chrome_exec,str) and chrome_exec != ''

        self._chrome_exe = chrome_exec
        self._sandbox = sandbox

        
    def html_to_pdf(self, html_byte_string, output_file, raise_exception=False):
        '''
        Converts the given html_byte_string to PDF stored at output_file

        html_byte_string (string) - html to be rendered to PDF
        output_file (File object) - file object to output PDF file  

        returns True if successful and False otherwise 
        '''

        # checks if the html string given is a valid string
        assert isinstance(html_byte_string,str)


        # create a temporary file to store the html
        with tempfile.NamedTemporaryFile(suffix='.html') as html_file:
            
            # write the contents to the file
            html_file.write(str.encode(html_byte_string))
            html_file.flush()

            temp_file_url = 'file://{0}'.format(html_file.name)

            print_to_pdf_command = self._generate_shell_command(
                self._chrome_exe, temp_file_url, output_file.name, self._sandbox,
            )

            isNotWindows = not sys.platform.startswith('win32')

            try:
                # execute the shell command to generate PDF
                subprocess.run(print_to_pdf_command,shell=isNotWindows,check=True)
            except subprocess.CalledProcessError:
                if raise_exception:
                    raise
                return False
            
        return True


    def _generate_shell_command(self, chrome_exe, input_url, output_file_name, sandbox):
        '''
        Generate the command string

        chrome_exe (string) - html to be rendered to PDF
        input_url (string) - html to be rendered to PDF
        output_file_name (string) - file object to output PDF file
        sandbox (boolean) - using sandbox mode

        returns command string
        '''

        args = ['{chrome_exec}'] + self._chrome_options

        if not sandbox:
            # Without sandbox
            args += ['--no-sandbox']

        args += ['--print-to-pdf={output_file}', '{input_url}']

        return ' '.join(args).format(
            chrome_exec=chrome_exe,
            input_url=input_url,
            output_file=output_file_name,
        )
