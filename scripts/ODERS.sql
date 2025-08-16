-- Table: public.orders

-- DROP TABLE IF EXISTS public.orders;

CREATE TABLE IF NOT EXISTS public.orders
(
    id uuid NOT NULL DEFAULT gen_random_uuid(),
    ma_dat_hang text COLLATE pg_catalog."default" NOT NULL,
    ma_hoa_don text COLLATE pg_catalog."default",
    ma_van_don text COLLATE pg_catalog."default",
    dia_chi_lay_hang text COLLATE pg_catalog."default",
    thoi_gian timestamp without time zone,
    thoi_gian_tao timestamp without time zone,
    ma_khach_hang text COLLATE pg_catalog."default",
    ten_khach_hang text COLLATE pg_catalog."default",
    dien_thoai text COLLATE pg_catalog."default",
    dia_chi_khach_hang text COLLATE pg_catalog."default",
    khu_vuc text COLLATE pg_catalog."default",
    phuong_xa text COLLATE pg_catalog."default",
    nguoi_nhan_dat text COLLATE pg_catalog."default",
    kenh_ban text COLLATE pg_catalog."default",
    nguoi_tao text COLLATE pg_catalog."default",
    doi_tac_giao_hang text COLLATE pg_catalog."default",
    nguoi_nhan text COLLATE pg_catalog."default",
    dien_thoai_nguoi_nhan text COLLATE pg_catalog."default",
    dia_chi_nguoi_nhan text COLLATE pg_catalog."default",
    khu_vuc_nguoi_nhan text COLLATE pg_catalog."default",
    xa_phuong_nguoi_nhan text COLLATE pg_catalog."default",
    dich_vu text COLLATE pg_catalog."default",
    trong_luong bigint,
    dai bigint,
    rong bigint,
    cao bigint,
    phi_tra_doi_tac_giao_hang numeric(18,2),
    ghi_chu text COLLATE pg_catalog."default",
    tong_tien_hang numeric(18,2),
    giam_gia_phieu_dat numeric(18,2),
    thu_khac numeric(18,2),
    khach_da_tra numeric(18,2),
    tien_mat numeric(18,2),
    the numeric(18,2),
    chuyen_khoan numeric(18,2),
    vi numeric(18,2),
    diem bigint,
    don_vi_tinh text COLLATE pg_catalog."default",
    thoi_gian_giao_hang timestamp without time zone,
    trang_thai text COLLATE pg_catalog."default",
    ma_hang text COLLATE pg_catalog."default",
    ma_vach text COLLATE pg_catalog."default",
    ten_hang text COLLATE pg_catalog."default",
    thuong_hieu text COLLATE pg_catalog."default",
    ghi_chu_hang_hoa text COLLATE pg_catalog."default",
    so_luong bigint,
    don_gia numeric(18,2),
    giam_gia_pham_tram numeric(18,2),
    giam_gia numeric(18,2),
    gia_ban numeric(18,2),
    thanh_tien numeric(18,2),
    CONSTRAINT orders_pkey PRIMARY KEY (id, ma_dat_hang)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.orders
    OWNER to haotran;