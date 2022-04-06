
nicoletfile = 'C:\Matlab\Patient93_LTM-1_t3.e';

% using low-level functions
hdr = ft_read_header(nicoletfile);
% dat = ft_read_data(nicoletfile, 'header', hdr);

% using high-level functions (recommended)
cfg            = [];
cfg.dataset    = nicoletfile;
cfg.continuous = 'yes';
cfg.channel    = 'all';
data           = ft_preprocessing(cfg);
dat            = data.trial{1};

ft_write_data('Patient93_LTM-1_t3.edf', dat, 'header', hdr);

% save('patient52_1.mat', '-v7.3')
% cfg.viewmode   = 'vertical';
% ft_databrowser(cfg, data);

