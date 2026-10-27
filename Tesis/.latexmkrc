$pdf_mode = 1;
$biber = '/home/ronal/.local/opt/biber/biber';
$max_repeat = 6;

add_cus_dep('glo', 'gls', 0, 'makeglossaries');

sub makeglossaries {
	system("makeglossaries $_[0]");
}
