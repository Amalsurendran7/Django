from django.urls import path,include
from .views import *

urlpatterns = [
     path('',uhome,name='uhome' ),
    path('myadmin',logi,name='adm' ),
    path('admhome',admhome,name='admhome' ),
      path('monthly_sales',monthly_sales,name='monthly_sales' ),
      path('sales',sales,name='sales' ),
        path('alo',lo,name='alo' ),
        path('filt/<int:price>',filt,name='filt' ),
            path('addp',admin_add_product_view,name='addp' ),
                path('update/<int:pk>',update_product_view,name='update' ),
                 path('del/<int:pk>',dele.as_view(),name='dele' ),
                 path('ulog',userlog,name='ulog' ),
                  path('signup',signup,name='signup' ),
                  path('ban',ban,name='ban' ),
                  path('orderdetail/<int:pk>',orderdetail.as_view(),name='orderdetail' ),
                   path('download/<int:productID>',download,name='download' ),
                   path('category/<slug:category_slug>/',uhome, name='products_by_category'),
                   path('admproduct',admproduct,name='admproduct'), 
                    path('ret/<int:id>',ret,name='ret'), 
                    path('u_address',u_address,name='u_address'), 
                      path('export_to_excel',export_to_excel,name='export_to_excel'), 
                       path('export_to_pdf',export_to_pdf,name='export_to_pdf'),
                       path('export_to_excel1',export_to_excel1,name='export_to_excel1'), 
                       path('export_to_pdf1',export_to_pdf1,name='export_to_pdf1'), 
                   
                 


                     
    path('userorder',userorder,name='userorder'), 
     path('wishpage/',wcart,name='wcart'), 
     path('editprofile/<int:user_id>',editprofile,name='editprofile'), 
                     
    path('validation/',validation,name='validation'), 
    path('changepass/<int:user_id>',changepass,name='changepass'), 
                   
                    path('addcart/<int:product_id>',wish_cart,name='wish_cart'),
    path('removecart/<int:product_id>/<int:cart_item_id>/',removewcart,name='removewcart'),
    path('remove_cart_item/<int:product_id>/<int:cart_item_id>/',remove_wcart_item,name='remove_wcart_item'),
    path('user_address',user_address,name='user_address' ),
   
                 
                   path('lo',ulo,name='lo' ),
                    path('detail/<int:pk>',detail.as_view(),name="detail"),
                    path('admuser',admuser,name="admuser"),
                    path('block/<int:pk>',block,name="block"),
                
                     path('emai',emai,name='emai'),
                      path('emailre',emailre,name='emailre'),
                      path('resend',resend,name='resend'),
                       path('orderview/',orderview,name='orderview'),
                        path('update_order/<int:id>/<int:t>/<int:k>',update_view,name='update_view'),
                            path('delete_order/<int:id>',delete_order,name='delete_order'),
                            path('user_delete_order/<int:id>',user_delete_order,name='user_delete_order'),
                      
                       path('otp',otp,name='otp'),
                       
                       path('profile',profile,name='profile'),
                       path('checking',checking,name='checking'),
                        
                    #   path('remove/<int:pk>',remove,name='remove'),
                         
                         path('adcancel/<int:id>',adcancel,name='adcancel'),     
                       path('verify',verifyi,name='verifyi'),
                       path('crecategory',cre.as_view(),name='cre'),
                        path('delet/<int:pk>',delet.as_view(),name='delet' ),
                         path('cat',cat,name='cat' ),
                          path('cupd/<pk>',cupd.as_view(),name='cupd' ),
                          

    
   
   




    
]
