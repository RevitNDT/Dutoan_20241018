#! python3
#--*--coding: utf-8 --*--

import tkinter as tk
from tkinter import ttk, LabelFrame
from tkinter.filedialog import asksaveasfilename
import pandas as pd

class CauKien:
    def __init__(self, parent, CK_type):
        self.frame = ttk.Frame(parent)
        self.entries = {}
        self.TenCK_type = CK_type  # Lưu loại cột

        # Tên của trường "Kích Thước Chân" sẽ thay đổi dựa vào CK_type
        main_field_name = "Kích Thước Thân" if CK_type == "CotHoiBien" else "Kích Thước Chân"

        # Danh sách các label và entry
        fields = [
            (main_field_name, True),
            ("Kích Thước Đầu", CK_type == "CotChinhBien"),
            ("Kích Thước Giữa Thân", False if CK_type in ["CotChinhBien", "CotHoiBien"] else True),
            ("Rộng Cánh", True),
            ("Dày Cánh", True),
            ("Dày Bụng", True),
            ("Dài Cấu Kiện (BM)", True)
        ]

        # Tạo label và entry cho từng trường
        for idx, (field_name, visible) in enumerate(fields):
            if visible:
                label = ttk.Label(self.frame, text=field_name)
                label.grid(row=idx, column=0, padx=5, pady=5, sticky="w")
                entry = ttk.Entry(self.frame)
                entry.grid(row=idx, column=1, padx=5, pady=5, sticky="we")
                self.entries[field_name] = entry

    def pack(self, **kwargs):
        self.frame.pack(**kwargs)

    def get_values(self):  # Trả về giá trị của các Entry dưới dạng từ điển        
        return {name: entry.get() for name, entry in self.entries.items()}

# Các hàm tính toán hình học
def calculate_rectangle_area(width, height, thick):
    kq = round((width * height * thick * 7850), 2)
    KL_HCN = '{}*{}*{}*7850={}'.format(width, height, thick, kq)
    return KL_HCN

def calculate_trapezoid_area(base1, base2, height):
    return (base1 + base2) * height / 2

# khối lượng cột chính biên
def mass_cot_chinh_bien(values):
    try:
        # Tính cánh (hình chữ nhật)
        rong_canh = float(values.get("Rộng Cánh", 0))
        day_canh = float(values.get("Dày Cánh", 0))
        dai_cau_kien = float(values.get("Dài Cấu Kiện (BM)", 0))
        area_canh = calculate_rectangle_area(rong_canh, dai_cau_kien, day_canh)

        # Tính bụng (hình thang)
        kich_thuoc_chan = float(values.get("Kích Thước Chân", 0))
        kich_thuoc_dau = float(values.get("Kích Thước Đầu", 0))
        day_bung = float(values.get("Dày Bụng", 0))
        area_bung = calculate_trapezoid_area(kich_thuoc_chan, kich_thuoc_dau, day_bung)

        return area_bung, area_canh
    except ValueError:
        return "Vui lòng nhập số hợp lệ."

# khối lượng cột hồi biên
def mass_cot_hoi_bien(values):
    try:
        # Tính cánh (hình chữ nhật)
        rong_canh = float(values.get("Rộng Cánh", 0))
        day_canh = float(values.get("Dày Cánh", 0))
        dai_cau_kien = float(values.get("Dài Cấu Kiện (BM)", 0))
        volum_canh = calculate_rectangle_area(rong_canh, dai_cau_kien, day_canh)

        # Tính bụng (hình thang)
        kich_thuoc_chan = float(values.get("Kích Thước Chân", 0))
        kich_thuoc_dau = float(values.get("Kích Thước Đầu", 0))
        day_bung = float(values.get("Dày Bụng", 0))
        volum_bung = calculate_trapezoid_area(kich_thuoc_chan, kich_thuoc_dau, day_bung)

        return volum_canh, volum_bung
    except ValueError:
        return "Vui lòng nhập số hợp lệ."

# Hàm tính toán độc lập, nhận đối tượng làm tham số
def calculate(KieuTenCauKien):
    values = KieuTenCauKien.get_values()
    if KieuTenCauKien.TenCK_type == "CotChinhBien":
        return mass_cot_chinh_bien(values)
    elif KieuTenCauKien.TenCK_type == "CotHoiBien":
        return mass_cot_hoi_bien(values)
    return "Không xác định loại cột."

def TinhToleVach():
    #Tole Vach Hông    
    DaiNha = (float(SL_KhungChinh.get())-1)*float(KC_BuocCotChinh.get())+2*float(KC_BuocCotHoi.get())+0.5
    CaoVachBenTruTuongXay = (float(Cao_VachBen.get())-float(KT_CaoTuongXay.get()))
    kq_KL_VachBen = 2*DaiNha*CaoVachBenTruTuongXay
    KL_ToleVachBen = '2*{}*{}={}'.format(DaiNha, CaoVachBenTruTuongXay,kq_KL_VachBen)
    #Tole Vach Hoi
    KL_TamGiac_VachHoi = ((float(KT_Nhip.get())*0.5)*(float(KT_Nhip.get())*0.5)*float(KT_DocMai.get())/100)     
    kq_ToleVachHoi = 2*(KL_TamGiac_VachHoi+float(KT_Nhip.get())*(float(Cao_VachBen.get())-float(KT_CaoTuongXay.get())))
    KT_Nhip_m = float(KT_Nhip.get())
    Cao_VachBen_m =float(Cao_VachBen.get())
    KL_ToleVachHoi = '2*({}*{}+{})={}'.format(KT_Nhip_m, Cao_VachBen_m, KL_TamGiac_VachHoi, kq_ToleVachHoi)
    # Trừ Cửa
    DT_CuaChinh = (float(Cao_CuaChinh.get()))*(float(Rong_CuaChinh.get()))
    DT_CuaPhu = (float(Cao_CuaPhu.get()))*(float(Rong_CuaPhu.get()))
    DT_CuaSo = (float(Cao_CuaSo.get()))*(float(Rong_CuaSo.get()))
    kq_DT_TruCua = DT_CuaChinh + DT_CuaPhu + DT_CuaSo
    Tru_KL_Cua = '-1*({}+{}+{})=-{}'.format(float(SL_CuaChinh.get()), DT_CuaChinh, DT_CuaSo ,kq_DT_TruCua)

    return ['Khối Lượng Tole Vách','Tole Vách Bên:',KL_ToleVachBen, 'Tole Vách Hồi:',KL_ToleVachHoi, 'DT Tole Trừ cửa:',Tru_KL_Cua]

def export_to_excel(results):
    # Chuyển đổi kết quả thành DataFrame với 1 cột duy nhất
    data_Khung = ["Khối Lượng Khung kèo"]
    for item in results:
        if len(item) == 2:  # Chỉ xử lý những phần tử có đúng 2 giá trị
            group_name, mass_info = item
            data_Khung.append(group_name)
            data_Khung.append(mass_info)

    # Tạo DataFrame 1
    data_Khung_dic = {
        'Mã Hiệu': ['TT'] + [''] * (len(data_Khung) - 1),
        'Diễn Giải KL': data_Khung,
        'Đơn Vị': ['kg'] + [''] * (len(data_Khung) - 1)
    }
    df1 = pd.DataFrame(data_Khung_dic)
       
    # Tạo DataFrame 2
    data_ToleVach = TinhToleVach() 
    data_ToleVach_dic = {
        'Mã Hiệu': ['TT'] + [''] * (len(data_ToleVach) - 1),
        'Diễn Giải KL': data_ToleVach,
        'Đơn Vị': ['m2'] + [''] * (len(data_ToleVach) - 1)
    }
    df2 = pd.DataFrame(data_ToleVach_dic)
    
    # Nối hai DataFrame
    df_Total = pd.concat([df1, df2], ignore_index=True)
    
    # Mở hộp thoại hỏi nơi lưu file
    root = tk.Tk()
    root.withdraw()  # Ẩn cửa sổ chính của Tkinter
    file_path = asksaveasfilename(
        initialfile="KL_NhaXuong.xlsx",  # Tên file mặc định
        defaultextension=".xlsx",
        filetypes=[("Excel Files", "*.xlsx"), ("All Files", "*.*")]
    )    
    if not file_path:
        return

    # Xuất DataFrame ra file Excel
    df_Total.to_excel(file_path, index=False)

def show_calculation_and_export():
    # Tính toán các giá trị
    result_CotHoiBien = calculate(cot_hoi_bien)
    result_CotChinhBien = calculate(cot_chinh_bien)

    # Tạo danh sách kết quả với tên cấu kiện và khối lượng
    results = []

    # Cột Hồi Biên
    if isinstance(result_CotHoiBien, tuple):
        results.append(("Cột Hồi Biên"))  # Tên nhóm
        results.append(("KL_Cánh_Cột_Hồi_Biên", result_CotHoiBien[0]))  # Khối lượng cánh
        results.append(("KL_Bụng_Cột_Hồi_Biên", result_CotHoiBien[1]))  # Khối lượng bụng

    # Cột Chính Biên
    if isinstance(result_CotChinhBien, tuple):
        results.append(("Cột Chính Biên"))  # Tên nhóm
        results.append(("KL_Cánh_Cột_Chính_Biên", result_CotChinhBien[0]))  # Khối lượng cánh
        results.append(("KL_Bụng_Cột_Chính_Biên", result_CotChinhBien[1]))  # Khối lượng bụng

    # Xuất ra Excel
    export_to_excel(results)

# Tạo tab TT_Cơ Bản
def create_tt_co_ban(notebook):
    tab_tt_co_ban = ttk.Frame(notebook)
    notebook.add(tab_tt_co_ban, text="TT_Cơ Bản")

    global KT_Nhip, KC_BuocCotChinh, SL_KhungChinh, KC_BuocCotHoi, KT_DocMai, Cao_VachBen, KT_CaoTuongXay, SL_CuaChinh, Cao_CuaChinh, Rong_CuaChinh, SL_CuaPhu, Cao_CuaPhu, Rong_CuaPhu, SL_CuaSo, Cao_CuaSo, Rong_CuaSo
    KT_Nhip = tk.StringVar()
    KC_BuocCotChinh = tk.StringVar()
    SL_KhungChinh = tk.StringVar()
    KC_BuocCotHoi = tk.StringVar()
    KT_DocMai = tk.StringVar()
    Cao_VachBen = tk.StringVar()
    KT_CaoTuongXay = tk.StringVar()
    SL_CuaChinh = tk.StringVar()
    Cao_CuaChinh = tk.StringVar()
    Rong_CuaChinh = tk.StringVar()
    SL_CuaPhu = tk.StringVar()
    Cao_CuaPhu = tk.StringVar()
    Rong_CuaPhu = tk.StringVar()
    SL_CuaSo = tk.StringVar()
    Cao_CuaSo = tk.StringVar()
    Rong_CuaSo = tk.StringVar()

    Basic_zone = LabelFrame(tab_tt_co_ban, text="THÔNG TIN CƠ BẢN", padx=10, pady=20)
    Basic_zone.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=10, pady=5)

    tk.Label(Basic_zone, text="Nhịp:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
    tk.Entry(Basic_zone, textvariable=KT_Nhip).grid(row=0, column=1, padx=5, pady=2)
    tk.Label(Basic_zone, text="Bước Cột Chính:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
    tk.Entry(Basic_zone, textvariable=KC_BuocCotChinh).grid(row=1, column=1, padx=5, pady=2)
    tk.Label(Basic_zone, text="Số Lượng Khung Chính:").grid(row=2, column=0, sticky="w", padx=5, pady=2)
    tk.Entry(Basic_zone, textvariable=SL_KhungChinh).grid(row=2, column=1, padx=5, pady=2)
    tk.Label(Basic_zone, text="Bước Cột Đầu Hồi:").grid(row=3, column=0, sticky="w", padx=5, pady=2)
    tk.Entry(Basic_zone, textvariable=KC_BuocCotHoi).grid(row=3, column=1, padx=5, pady=2)

    tk.Label(Basic_zone, text="Dốc Mái:").grid(row=4, column=0, sticky="w", padx=5, pady=2)
    tk.Entry(Basic_zone, textvariable=KT_DocMai).grid(row=4, column=1, padx=5, pady=2)
    tk.Label(Basic_zone, text="Cao Vách Hông(Cả Tường):").grid(row=5, column=0, sticky="w", padx=5, pady=2)
    tk.Entry(Basic_zone, textvariable=Cao_VachBen).grid(row=5, column=1, padx=5, pady=2)

    tk.Label(Basic_zone, text="Cao Tường Xây:").grid(row=6, column=0, sticky="w", padx=5, pady=2)
    tk.Entry(Basic_zone, textvariable=KT_CaoTuongXay).grid(row=6, column=1, padx=5, pady=2)

    tk.Label(Basic_zone, text="Số Lượng Cửa Chính:").grid(row=0, column=2, sticky="w", padx=5, pady=2)
    tk.Entry(Basic_zone, textvariable=SL_CuaChinh).grid(row=0, column=3, padx=5, pady=2)
    tk.Label(Basic_zone, text="Cao Cửa Chính:").grid(row=1, column=2, sticky="w", padx=5, pady=2)
    tk.Entry(Basic_zone, textvariable=Cao_CuaChinh).grid(row=1, column=3, padx=5, pady=2)
    tk.Label(Basic_zone, text="Rộng Cửa Chính:").grid(row=2, column=2, sticky="w", padx=5, pady=2)
    tk.Entry(Basic_zone, textvariable=Rong_CuaChinh).grid(row=2, column=3, padx=5, pady=2)
    tk.Label(Basic_zone, text="Số Lượng Cửa Phụ:").grid(row=3, column=2, sticky="w", padx=5, pady=2)
    tk.Entry(Basic_zone, textvariable=SL_CuaPhu).grid(row=3, column=3, padx=5, pady=2)
    tk.Label(Basic_zone, text="Cao Cửa Phụ:").grid(row=4, column=2, sticky="w", padx=5, pady=2)
    tk.Entry(Basic_zone, textvariable=Cao_CuaPhu).grid(row=4, column=3, padx=5, pady=2)
    tk.Label(Basic_zone, text="Rộng Cửa Phụ:").grid(row=5, column=2, sticky="w", padx=5, pady=2)
    tk.Entry(Basic_zone, textvariable=Rong_CuaPhu).grid(row=5, column=3, padx=5, pady=2)
    tk.Label(Basic_zone, text="Số Lượng Cửa Sổ:").grid(row=6, column=2, sticky="w", padx=5, pady=2)
    tk.Entry(Basic_zone, textvariable=SL_CuaSo).grid(row=6, column=3, padx=5, pady=2)
    tk.Label(Basic_zone, text="Cao Cửa Sổ:").grid(row=7, column=2, sticky="w", padx=5, pady=2)
    tk.Entry(Basic_zone, textvariable=Cao_CuaSo).grid(row=7, column=3, padx=5, pady=2)
    tk.Label(Basic_zone, text="Rộng Cửa Sổ:").grid(row=8, column=2, sticky="w", padx=5, pady=2)
    tk.Entry(Basic_zone, textvariable=Rong_CuaSo).grid(row=8, column=3, padx=5, pady=2)







    # Vùng "NÓC GIÓ"
    global Nhip_NocGio, Cao_Cot_NocGio, TietDien_Ngang_Thanh, TietDien_Dung_Thanh, Day_Thanh, Loai_Thanh, Enable_NocGio
    Nhip_NocGio = tk.StringVar()
    Cao_Cot_NocGio = tk.StringVar()
    TietDien_Ngang_Thanh = tk.StringVar()
    TietDien_Dung_Thanh = tk.StringVar()
    Day_Thanh = tk.StringVar()
    Loai_Thanh = tk.StringVar()
    Enable_NocGio = tk.BooleanVar()

    NocGio_zone = LabelFrame(tab_tt_co_ban, text="THÔNG TIN NÓC GIÓ", padx=10, pady=20)
    NocGio_zone.grid(row=0, column=1, sticky="new", padx=10, pady=5)

    # Checkbox "Bật/Tắt Nóc Gió"
    NocGio_zone_check = ttk.Checkbutton(NocGio_zone, text="Bật/Tắt Nóc Gió", variable=Enable_NocGio, command=lambda: on_toggle_noc_gio(NocGio_zone, Enable_NocGio))
    NocGio_zone_check.grid(row=0, columnspan=2, sticky="w", padx=5, pady=2)

    # Thêm Label và ComboBox
    tk.Label(NocGio_zone, text="Loại Thanh:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
    combobox_loai_thanh = ttk.Combobox(NocGio_zone, textvariable=Loai_Thanh, values=["Thanh i", "Thanh Hộp"], width=17, state="readonly")
    combobox_loai_thanh.grid(row=1, column=1, padx=5, pady=2)

    tk.Label(NocGio_zone, text="Nhịp Nóc Gió:").grid(row=2, column=0, sticky="w", padx=5, pady=2)
    entry_nhip_nocgio = tk.Entry(NocGio_zone, textvariable=Nhip_NocGio, state="normal" if Enable_NocGio.get() else "disabled")
    entry_nhip_nocgio.grid(row=2, column=1, padx=5, pady=2)
    tk.Label(NocGio_zone, text="Cao Cột Nóc Gió:").grid(row=3, column=0, sticky="w", padx=5, pady=2)
    entry_cao_cot_nocgio = tk.Entry(NocGio_zone, textvariable=Cao_Cot_NocGio, state="normal" if Enable_NocGio.get() else "disabled")
    entry_cao_cot_nocgio.grid(row=3, column=1, padx=5, pady=2)
    tk.Label(NocGio_zone, text="Tiết Diện Ngang Thanh:").grid(row=4, column=0, sticky="w", padx=5, pady=2)
    entry_tietdien_ngang_thanh = tk.Entry(NocGio_zone, textvariable=TietDien_Ngang_Thanh, state="normal" if Enable_NocGio.get() else "disabled")
    entry_tietdien_ngang_thanh.grid(row=4, column=1, padx=5, pady=2)
    tk.Label(NocGio_zone, text="Tiết Diện Dọc Thanh:").grid(row=5, column=0, sticky="w", padx=5, pady=2)
    entry_tietdien_dung_thanh = tk.Entry(NocGio_zone, textvariable=TietDien_Dung_Thanh, state="normal" if Enable_NocGio.get() else "disabled")
    entry_tietdien_dung_thanh.grid(row=5, column=1, padx=5, pady=2)
    tk.Label(NocGio_zone, text="Dày Thanh:").grid(row=6, column=0, sticky="w", padx=5, pady=2)
    entry_day_thanh = tk.Entry(NocGio_zone, textvariable=Day_Thanh, state="normal" if Enable_NocGio.get() else "disabled")
    entry_day_thanh.grid(row=6, column=1, padx=5, pady=2)

    def on_toggle_noc_gio(NocGio_zone, Enable_NocGio):
        state = "normal" if Enable_NocGio.get() else "disabled"
        color = "black" if Enable_NocGio.get() else "gray"  # Màu chữ cho Label
        for widget in NocGio_zone.winfo_children():
            if isinstance(widget, (tk.Entry, ttk.Combobox)):
                widget.configure(state=state)
            elif isinstance(widget, tk.Label):
                widget.configure(foreground=color)




    # Vùng "XÀ GỒ"
    global SoHang_XG_Vach, SoHang_XG_Mai, Cao_XG_Vach, Cao_XG_Mai, Day_XG_Vach, Day_XG_Mai, SoHang_TiGiang_XG
    SoHang_XG_Vach = tk.StringVar()
    SoHang_XG_Mai = tk.StringVar()
    Cao_XG_Vach = tk.StringVar()
    Cao_XG_Mai = tk.StringVar()
    Day_XG_Vach = tk.StringVar()
    Day_XG_Mai = tk.StringVar()
    SoHang_TiGiang_XG = tk.StringVar()
    Enable_XG = tk.BooleanVar()

    XaGo_zone = LabelFrame(tab_tt_co_ban, text="THÔNG TIN XÀ GỒ", padx=10, pady=20)
    XaGo_zone.grid(row=1, column=1, sticky="new", padx=10, pady=5)

    tk.Label(XaGo_zone, text="Số Hàng XG Vách:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
    entry_SoHang_XG_Vach = tk.Entry(XaGo_zone, textvariable=SoHang_XG_Vach)
    entry_SoHang_XG_Vach.grid(row=0, column=1, padx=5, pady=2)




    # Nút tính toán và xuất Excel
    calculate_button = ttk.Button(tab_tt_co_ban, text="Tính Toán & Xuất Excel", command=show_calculation_and_export)
    calculate_button.grid(row=2, column=0, columnspan=2, sticky="e", padx=10, pady=10)

    on_toggle_noc_gio(NocGio_zone, Enable_NocGio)  # Gọi hàm để mờ các widget ngay từ đầu

    return tab_tt_co_ban



# Tạo tab TT_Cột
def create_tt_cot(notebook):
    tab_tt_cot = ttk.Frame(notebook)
    notebook.add(tab_tt_cot, text="TT_Cột")

    # Vùng Cột Chính Biên
    cot_chinh_bien_frame = ttk.LabelFrame(tab_tt_cot, text="Cột Chính Biên")
    cot_chinh_bien_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    cot_chinh_bien = CauKien(cot_chinh_bien_frame, "CotChinhBien")
    cot_chinh_bien.pack(fill="both", expand=True)

    # Vùng Cột Hồi Biên
    cot_hoi_bien_frame = ttk.LabelFrame(tab_tt_cot, text="Cột Hồi Biên")
    cot_hoi_bien_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
    cot_hoi_bien = CauKien(cot_hoi_bien_frame, "CotHoiBien")
    cot_hoi_bien.pack(fill="both", expand=True)

    return tab_tt_cot, cot_chinh_bien, cot_hoi_bien


def create_dam_tab(notebook):
    tab_dam = ttk.Frame(notebook)
    notebook.add(tab_dam, text="Dầm")

    # Tạo lưới 3 cột cho 3 khu vực
    tab_dam.columnconfigure((0, 1, 2), weight=1)

    # Khu vực Dầm Chân Kèo
    frame_dam_chan_keo = ttk.LabelFrame(tab_dam, text="Dầm Chân Kèo")
    frame_dam_chan_keo.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    dam_chan_keo = CauKien(frame_dam_chan_keo, "DamChanKeo")
    dam_chan_keo.pack(fill="x")

    # Khu vực Dầm Giữa
    frame_dam_giua = ttk.LabelFrame(tab_dam, text="Dầm Giữa")
    frame_dam_giua.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
    dam_giua_checkbox = tk.IntVar()
    dam_giua_enable = ttk.Checkbutton(
        frame_dam_giua,
        text="Bật/Tắt Dầm Giữa",
        variable=dam_giua_checkbox,
        command=lambda: toggle_dam_section(dam_giua, dam_giua_checkbox.get())
    )
    dam_giua_enable.pack(anchor="w")
    dam_giua = CauKien(frame_dam_giua, "DamGiua")
    dam_giua.pack(fill="x")

    # Khu vực Dầm Đỉnh
    frame_dam_dinh = ttk.LabelFrame(tab_dam, text="Dầm Đỉnh")
    frame_dam_dinh.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
    dam_dinh_checkbox = tk.IntVar()
    dam_dinh_enable = ttk.Checkbutton(
        frame_dam_dinh,
        text="Bật/Tắt Dầm Đỉnh",
        variable=dam_dinh_checkbox,
        command=lambda: toggle_dam_section(dam_dinh, dam_dinh_checkbox.get())
    )
    dam_dinh_enable.pack(anchor="w")
    dam_dinh = CauKien(frame_dam_dinh, "DamDinh")
    dam_dinh.pack(fill="x")

    # Khu vực Thông Tin Mở Rộng Đỉnh Kèo
    frame_mo_rong_dinh_keo = ttk.LabelFrame(tab_dam, text="Phần Mở Rộng Đỉnh Kèo")
    frame_mo_rong_dinh_keo.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

    global cao_tamgiac_dinhkeo
    cao_tamgiac_dinhkeo = tk.StringVar()
    global dai_tamgiac_dinhkeo
    dai_tamgiac_dinhkeo = tk.StringVar()

    ttk.Label(frame_mo_rong_dinh_keo, text="Cao Tam Giác Mở Rộng Đỉnh Kèo:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
    cao_tam_giac_entry = ttk.Entry(frame_mo_rong_dinh_keo, textvariable=cao_tamgiac_dinhkeo)
    cao_tam_giac_entry.grid(row=1, column=1, padx=5, pady=2)

    ttk.Label(frame_mo_rong_dinh_keo, text="Dài Tam Giác Mở Rộng Đỉnh Kèo:").grid(row=2, column=0, sticky="w", padx=5, pady=2)
    dai_tam_giac_entry = ttk.Entry(frame_mo_rong_dinh_keo, textvariable=dai_tamgiac_dinhkeo)
    dai_tam_giac_entry.grid(row=2, column=1, padx=5, pady=2)

    mo_rong_dinh_keo_checkbox = tk.IntVar()
    mo_rong_dinh_keo_enable = ttk.Checkbutton(
        frame_mo_rong_dinh_keo,
        text="Bật/Tắt Mở Rộng Đỉnh Kèo",
        variable=mo_rong_dinh_keo_checkbox,
        command=lambda: toggle_mo_rong_section(frame_mo_rong_dinh_keo, mo_rong_dinh_keo_checkbox.get())
    )
    mo_rong_dinh_keo_enable.grid(row=0, column=0, columnspan=2, sticky="w", padx=5, pady=2)

    # Mặc định tắt các phần
    toggle_dam_section(dam_giua, 0)
    toggle_dam_section(dam_dinh, 0)
    toggle_mo_rong_section(frame_mo_rong_dinh_keo, 0)


def toggle_dam_section(dam_section, enabled):
    state = "normal" if enabled else "disabled"
    for widget in dam_section.frame.winfo_children():
        widget.configure(state=state)


def toggle_mo_rong_section(frame, enabled):
    state = "normal" if enabled else "disabled"
    color = "black" if enabled else "gray"
    for widget in frame.winfo_children():
        if isinstance(widget, ttk.Entry):
            widget.configure(state=state)
        elif isinstance(widget, ttk.Label):
            widget.configure(foreground=color)

# Cửa sổ chính và Notebook
root = tk.Tk()
root.title("RevitNDT_Khối Lượng Nhà Xưởng")

notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")

create_tt_co_ban(notebook)
create_dam_tab(notebook)
# Tạo tab TT_Cột sau khi đã có đủ thông tin từ TT_Cơ Bản
tab_tt_cot, cot_chinh_bien, cot_hoi_bien = create_tt_cot(notebook)

root.mainloop()

#print (float(KT_DocMai.get())+1)