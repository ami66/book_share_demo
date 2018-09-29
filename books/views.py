from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.views.generic import View

from .models import Book, Category


class BookListView(View):
    """
    图书列表
    """
    def get(self, request):
        # 当前页面
        current_page = 'book_list'
        # 取出所有图书
        books = Book.objects.all()
        # 取出所有图书分类
        categories = Category.objects.all()

        # 获取前端传入的分类id, 默认0是全部分类
        current_category_id = request.GET.get('category', 0)

        fake_books = [1, 2, 3, 4, 5]

        if current_category_id:
            books = books.filter(category_id=int(current_category_id))
            # 家测试图书数据
            fake_books = list(range(0, len(books) * 10))

        return render(request, 'book-list.html', {
            'books': books,
            'fake_books': fake_books,
            'categories': categories,
            'current_page': current_page,
            'current_category_id': current_category_id,
        })


class BookDetailView(View):
    """
    图书详情页面
    """
    def get(self, request, book_id):
        book = get_object_or_404(Book, id=int(book_id))
        data = request.GET.get('data', 'recent')
        comments, info = self.get_comments(book, data)
        return render(request, 'book-detail.html', {
            'book': book,
            'comments': comments,
            'comment_count': len(comments),
            'info': info,
            'data': data,
        })

    def get_comments(self, book, data):
        """
        :param book:
        :param data:
        :return: 如果data==recent则返回最新书评，如果data==hot则返回精彩评论，其他情况则返回[]
        """
        if data == 'recent':
            comments = book.comments.all().order_by('-created')
            info = '最新'
        elif data == 'hot':
            # 可根据书评点赞书进行降序排序
            comments = book.comments.all()
            info = '精彩'
        else:
            comments = []
            info = '暂无'
        return comments, info
